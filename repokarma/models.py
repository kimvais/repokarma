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

from django.db import models
from mercurial import hg, ui


class EMail(models.Model):
    address = models.CharField(max_length=512)
    user = models.ForeignKey("repokarma.User", related_name="email")
    class Meta:
        app_label = "repokarma"


class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    real_name = models.CharField(max_length=512, null=True)
    class Meta:
        app_label = "repokarma"

    @property
    def name(self):
        if self.real_name:
            return self.real_name
        return self.username


class Repository(models.Model):
    path = models.CharField(max_length=1024)
    repository_type = models.CharField(max_length=32)

    class Meta:
        unique_together = ('path', 'repository_type')


class Commit(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    repository = models.ForeignKey('repokarma.Repository')
    nodeid = models.IntegerField(null=True)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User)
    lines_added = models.IntegerField()
    lines_removed = models.IntegerField()
    description = models.TextField()

    def __init__(self, *args, **kwargs):
        super(Commit, self).__init__(*args, **kwargs)
        self.diffs = None
        self.context = None
        if self.pk:
            try:
                repotype = self.repository.repository_type
            except Repository.DoesNotExist:
                repotype = None
            if repotype == "mercurial":
                self._get_hg_changeset()
            elif repotype == 'git':
                # TODO
                pass

    def _get_hg_changeset(self):
        repo = hg.repository(ui.ui(), self.repository.path)
        self.context = repo.changectx(self.pk)
        self.diffs = list()
        for diff in self.context.diff():
            self.diffs.append(Diff(diff))

    @property
    def net_change(self):
        return self.lines_added - self.lines_removed

    @property
    def files(self):
        return self.context.files

    @property
    def filecount(self):
        return len(self.context.files)

    @property
    def parents(self):
        if self.repository.repository_type == "mercurial":
            return [c.hex() for c in self.context.parents()]

    @property
    def children(self):
        if self.repository.repository_type == "mercurial":
            return [c.hex() for c in self.context.children()]

    class Meta:
        app_label = "repokarma"
        get_latest_by = 'timestamp'
        ordering = ['-timestamp']


class Diff(object):
    def __init__(self, data):
        self.data = data
        self.cmd = data.split('\n', 1)[0]
        self.filename = self.cmd.rsplit(' ', 1)[-1]