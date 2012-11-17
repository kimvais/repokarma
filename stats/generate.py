#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2012 Kimmo Parviainen-Jalanko <k@77.fi>
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
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist
from mercurial import hg, ui
from models import ChangeSet, HGUser


try:
    start = ChangeSet.objects.latest().pk
except ObjectDoesNotExist:
    start = 0

repo = hg.repository(ui.ui(), settings.REPO_PATH)
tip = repo.revs("default")[0]
print "Fetching revisions {0}-{1}".format(start, tip)
for rev in range(start, tip):
    adds = removes = 0
    ctx = repo.changectx(rev)
    user, _ = HGUser.objects.get_or_create(name=ctx.user())
    timestamp = datetime.fromtimestamp(ctx.date()[0]).isoformat()
    if len(ctx.parents()) > 1:
        print "skipping merge {0}".format(rev)
        continue
    for filecount, diff in enumerate(ctx.diff()):
        diffcmd, diffdata = diff.split('\n', 1)
        #print diffcmd
        if "3rdparty" in diffcmd:
            print "skipping 3rd party component {0}".format(
                diffcmd.rsplit(' ', 1)[-1])
            continue
            #print fromfile.rsplit(' ', 1)[-1]
        #print tofile.rsplit(' ', 1)[-1]
        for line in diffdata:
            if line.startswith('Binary'):
                print "Skipping binary file".format(
                    diffcmd.rsplit(' ', 1)[-1])
                break
            if line.startswith('+'):
                adds += 1
            elif line.startswith('-'):
                removes += 1
    changeset = ChangeSet(revision=rev,
                          timestamp=timestamp,
                          user=user,
                          lines_added=adds,
                          lines_removed=removes,
                          files=filecount,
                          description=ctx.description())
    changeset.save()
    print "{0},'{1}',{2},{3}".format(timestamp, user.name, adds, removes)
