# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 Cidadanía Coop.
# Written by: Oscar Carballal Prego <info@oscarcp.com>
#
# This file is part of e-cidadania.
#
# e-cidadania is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# e-cidadania is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with e-cidadania. If not, see <http://www.gnu.org/licenses/>.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import FormView

from django.template import RequestContext
from django.views.generic.create_update import create_object
from django.views.generic.create_update import update_object

from django.contrib.auth.models import User
from e_cidadania.apps.spaces.models import Space
from e_cidadania.apps.news.models import Post
from e_cidadania.apps.news.forms import NewsForm


class AddPost(FormView):

    """
    Create a new post. Only registered users belonging to a concrete group
    are allowed to create news. only site administrators will be able to
    post news in the index page.
    """
    form_class = NewsForm
    template_name = 'news/post_add.html'
    
    def get_success_url(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_name'])
        return '/spaces/' + self.space.url
        
    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_name'])
        form_uncommited = form.save(commit=False)
        form_uncommited.author = self.request.user
        form_uncommited.space = self.space
        form_uncommited.save()
        return super(AddPost, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddPost, self).get_context_data(**kwargs)
        self.space = get_object_or_404(Space, url=self.kwargs['space_name'])
        context['get_place'] = self.space
        return context
        
    @method_decorator(permission_required('news.add_post'))
    def dispatch(self, *args, **kwargs):
        return super(AddPost, self).dispatch(*args, **kwargs)


class ViewPost(DetailView):

    """
    View a specific post.
    """
    context_object_name = 'news'
    template_name = 'news/post_detail.html'

    def get_object(self):
        return Post.objects.get(pk=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):

        """
        Get extra context data for the ViewPost view.
        """
        context = super(ViewPost, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        return context


class EditPost(UpdateView):

    """
    Edit an existent post.
    """
    model = Post
    template_name = 'news/post_edit.html'

    def get_success_url(self):
        self.space = get_object_or_404(Space, url=self.kwargs['space_name'])
        return '/spaces/' + self.space.url

    def get_object(self):
        cur_post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return cur_post
        
    def get_context_data(self, **kwargs):
        context = super(EditPost, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        return context
        
    @method_decorator(permission_required('news.edit_post'))
    def dispatch(self, *args, **kwargs):
        return super(EditPost, self).dispatch(*args, **kwargs)


class DeletePost(DeleteView):

    """
    Delete an existent post. Post deletion is only reserved to spaces
    administrators or site admins.
    """
    context_object_name = "get_place"

    def get_success_url(self):
        space = self.kwargs['space_name']
        return '/spaces/%s' % (space)

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):

        """
        Get extra context data for the ViewPost view.
        """
        context = super(DeletePost, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        return context

