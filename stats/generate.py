#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 SSH Communication Security Corporation.
# All rights reserved.
# This software is protected by international copyright laws.
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
