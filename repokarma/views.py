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
from django.conf import settings
from django.views.generic import ListView, TemplateView
from infinite_pagination import InfinitePaginator

from mercurial import hg, ui
from . import models
from repokarma.models import HGDiff


class ChangeLog(ListView):
    model = models.Commit
    template_name = "changelog.html"
    paginator_class = InfinitePaginator
    paginate_by = 30

    def get_context_object_name(self, object_list):
        return "revision"


class Users(ListView):
    model = models.User
    template_name = "userlist.html"

    def get_context_object_name(self, object_list):
        return 'users'


class Commit(TemplateView):
    template_name = "changeset.html"

    def get_context_data(self, **kwargs):
        ctx = super(TemplateView, self).get_context_data(**kwargs)
        ctx['changeset'] = models.Commit.objects.get(pk=self.rev)
        return ctx

    def dispatch(self, request, *args, **kwargs):
        self.rev = kwargs.pop('rev')
        return super(TemplateView, self).dispatch(request, *args, **kwargs)