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

"""
Proposal module views.
"""

# Generic class-based views
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import FormView

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.utils.decorators import method_decorator

from django.views.generic.create_update import update_object
from django.db.models import F
from django.http import HttpResponse

from e_cidadania.apps.proposals.models import Proposal
from e_cidadania.apps.proposals.forms import ProposalForm, VoteProposal
from e_cidadania.apps.spaces.models import Space


class AddProposal(FormView):

    """
    Create a new proposal.

    :rtype: HTML Form
    :context: form, get_place
    """
    form_class = ProposalForm
    template_name = 'proposals/proposal_add.html'
    
    def get_success_url(self):
        return '/spaces/' + self.kwargs['space_name']
    
    def form_valid(self, form):
        self.space = get_object_or_404(Space, url=self.kwargs['space_name'])
        form_uncommited = form.save(commit=False)
        form_uncommited.space = self.space
        form_uncommited.author = self.request.user
        form_uncommited.save()
        return super(AddProposal, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(AddProposal, self).get_context_data(**kwargs)
        self.space = get_object_or_404(Space, url=self.kwargs['space_name'])
        context['get_place'] = self.space
        return context
        
    @method_decorator(permission_required('proposals.add_proposal'))
    def dispatch(self, *args, **kwargs):
        return super(AddProposal, self).dispatch(*args, **kwargs)


class ViewProposal(DetailView):

    """
    Detail view of a proposal. Inherits from django :class:`DetailView` generic
    view.

    :rtype: object
    :context: proposal
    """
    context_object_name = 'proposal'
    template_name = 'proposals/proposal_detail.html'

    def get_object(self):
        prop_id = self.kwargs['prop_id']
        return get_object_or_404(Proposal, pk = prop_id)

    def get_context_data(self, **kwargs):
        context = super(ViewProposal, self).get_context_data(**kwargs)
        support_votes_count = Proposal.objects.annotate(Count('support_votes'))
        current_proposal = int(self.kwargs['prop_id']) - 1
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        context['support_votes_count'] = support_votes_count[current_proposal].support_votes__count
        return context


class EditProposal(UpdateView):

    """
    The proposal can be edited by space and global admins, but also by their
    creator.

    :rtype: HTML Form
    :context: get_place
    """
    model = Proposal
    template_name = 'proposals/proposal_edit.html'
    
    def get_success_url(self):
        return '/spaces/{0}/proposal/{1}/'.format(self.kwargs['space_name'], self.kwargs['prop_id'])
        
    def get_object(self):
        prop_id = self.kwargs['prop_id']
        return get_object_or_404(Proposal, pk = prop_id)
        
    def get_context_data(self, **kwargs):
        context = super(EditProposal, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        return context
        
    @method_decorator(permission_required('proposals.edit_proposal'))
    def dispatch(self, *args, **kwargs):
        return super(EditProposal, self).dispatch(*args, **kwargs)
                             
            
class DeleteProposal(DeleteView):

    """
    Delete a proposal.

    :rtype: Confirmation
    :context: get_place
    """
    def get_object(self):
        return get_object_or_404(Proposal, pk = self.kwargs['prop_id'])

    def get_success_url(self):
        current_space = self.kwargs['space_name']
        return '/spaces/{0}'.format(current_space)

    def get_context_data(self, **kwargs):
        context = super(DeleteProposal, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        return context                 
                  
           
@require_POST
def vote_proposal(request, space_name):

    """
    Increment support votes for the proposal in 1.
    """
    prop = get_object_or_404(Proposal, pk=request.POST['propid'])
#    if Proposal.objects.filter(support_votes__contains=request.user):
#        return HttpResponse("You already voted")
#    else:
    prop.support_votes.add(request.user)
    return HttpResponse("Vote emmited.")


class ListProposals(ListView):

    """
    List all proposals stored whithin a space. Inherits from django :class:`ListView`
    generic view.

    :rtype: Object list
    :context: proposal
    """
    paginate_by = 50
    context_object_name = 'proposal'

    def get_queryset(self):
        place = get_object_or_404(Space, url=self.kwargs['space_name'])
        objects = Proposal.objects.annotate(Count('support_votes')).filter(space=place.id).order_by('pub_date')
        return objects

    def get_context_data(self, **kwargs):
        context = super(ListProposals, self).get_context_data(**kwargs)
        context['get_place'] = get_object_or_404(Space, url=self.kwargs['space_name'])
        return context

