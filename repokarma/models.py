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


class EMail(models.Model):
    address = models.CharField(max_length=512)
    user = models.ForeignKey("repokarma.HGUser", related_name="email")
    class Meta:
        app_label = "repokarma"


class HGUser(models.Model):
    username = models.CharField(max_length=64, unique=True)
    real_name = models.CharField(max_length=512, null=True)
    class Meta:
        app_label = "repokarma"


class ChangeSet(models.Model):
    revision = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(HGUser)
    files = models.IntegerField()
    lines_added = models.IntegerField()
    lines_removed = models.IntegerField()
    description = models.TextField()

    @property
    def net_change(self):
        return self.lines_added - self.lines_removed

    class Meta:
        app_label = "repokarma"
        get_latest_by = 'timestamp'

