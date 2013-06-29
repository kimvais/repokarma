#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2012-2013 Kimmo Parviainen-Jalanko <k@77.fi>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
from datetime import datetime
import logging
import re
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from repokarma import models

logger = logging.getLogger(__name__)
logging.basicConfig()


def get_user(email, realname, username):
    user, _ = models.User.objects.get_or_create(username=username)
    if user.real_name is None:
        user.real_name = realname
        user.save()
    email_o, created = models.EMail.objects.get_or_create(address=email,
                                                          user=user)
    if created:
        email_o.save()
    return user


def sync_mercurial(repo_obj):
    from mercurial import hg, ui

    repo = hg.repository(ui.ui(), repo_obj.path)
    try:
        start = models.Commit.objects.all().aggregate(Max('nodeid'))[
                    'nodeid__max'] + 1
    except ObjectDoesNotExist:
        start = 0
    user_with_email_re = re.compile('^(.+) <(.+)>')
    tip = repo.revs("default")[0] + 1
    print("Fetching revisions {0}-{1}".format(start, tip - 1))
    for rev in range(start, tip):
        adds = removes = 0
        ctx = repo.changectx(rev)
        ctx_user = ctx.user()
        m = user_with_email_re.match(ctx_user)
        if m:
            realname = m.group(1)
            email = m.group(2)
        else:
            realname = None
            email = ctx_user
        username = email.split('@')[0]
        user = get_user(email, realname, username)

        timestamp = datetime.fromtimestamp(ctx.date()[0]).isoformat()
        if len(ctx.parents()) > 1:
            print("skipping merge {0}".format(rev))
            continue
        for filecount, diff in enumerate(ctx.diff()):
            diffcmd, diffdata = diff.split('\n', 1)
            #print diffcmd
            if "3rdparty" in diffcmd:
                print("skipping 3rd party component {0}".format(
                    diffcmd.rsplit(' ', 1)[-1]))
                continue
                #print fromfile.rsplit(' ', 1)[-1]
            #print tofile.rsplit(' ', 1)[-1]
            for line in diffdata:
                if line.startswith('Binary'):
                    print("Skipping binary file".format(
                        diffcmd.rsplit(' ', 1)[-1]))
                    break
                if line.startswith('+'):
                    adds += 1
                elif line.startswith('-'):
                    removes += 1
        changeset = models.Commit(id=ctx.hex(),
                                  nodeid=rev,
                                  timestamp=timestamp,
                                  user=user,
                                  lines_added=adds,
                                  lines_removed=removes,
                                  files=filecount,
                                  repository=repo_obj,
                                  description=ctx.description())
        changeset.save()
        print("{0},'{1}',{2},{3}".format(timestamp, user.username, adds,
                                         removes))


def sync_git(repo):
    import git

    r = git.Repo(repo.path)
    for commit in r.iter_commits('master'):
        try:
            _ = models.Commit.objects.get(id=commit.hexsha)
        except models.Commit.DoesNotExist:
            co = models.Commit()
            co.pk = commit.hexsha
            co.nodeid = None
            co.timestamp = datetime.fromtimestamp(min(commit.authored_date,
                                                      commit.committed_date))
            user = get_user(commit.author.email,
                            commit.author.email.split(
                                '@')[0],
                            commit.author.name)
            co.user = user
            stats = commit.stats.total
            co.lines_added = stats['insertions']
            co.lines_removed = stats['deletions']
            # co.files = stats['files']
            co.repository = repo
            co.description = commit.message
            co.save()
            print("{0},'{1}',{2},{3}".format(co.timestamp, user.username,
                                             co.lines_added,
                                             co.lines_removed))


if __name__ == '__main__':
    repo_obj, created = models.Repository.objects.get_or_create(

        repository_type=settings.REPO_TYPE,
        path=settings.REPO_PATH,
    )
    if created:
        repo_obj.save()
    sync_func = locals().get('sync_{0}'.format(settings.REPO_TYPE))
    sync_func(repo_obj)
