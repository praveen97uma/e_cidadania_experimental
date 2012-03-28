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

import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from e_cidadania.apps.userprofile.models import BaseProfile
from e_cidadania.apps.spaces.models import Space

GENDER = (

    ('M', _('Male')),
    ('F', _('Female')),

)

class Interest(models.Model):

    """
    """
    item = models.CharField(_('Interes'), max_length=50)

class UserProfile(BaseProfile):


    """
    Extends the default User profiles of Django. The fields of this model
    can be obtained by the user.get_profile method and it's extended by the
    django-profile application.
    """
    #user = models.ForeignKey(User, unique=True)
    
    firstname = models.CharField(_('Name'), max_length=50, blank=True)
    surname = models.CharField(_('Surname'), max_length=200, blank=True)
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER,
                              blank=True)
    
    birthdate = models.DateField(_('Birth date'), default=datetime.date.today(),
                                 blank=True)
    
    # Maybe one day this will be replaced by a list of choices.
    province = models.CharField(_('Province'), max_length=50)
    region = models.CharField(_('Region'), max_length=50)
    neighborhood = models.CharField(_('Neighborhood'), max_length=50)
    
    # Detailed overview of the address
    address = models.CharField(_('Address'), max_length=100)
    address_number = models.CharField(_('Number'), max_length=3, blank=True,
                                      null=True)
    address_floor = models.CharField(_('Floor'), max_length=3)
    address_letter = models.CharField(_('Letter'), max_length=2, null=True,
                                      blank=True)
    
    phone = models.CharField(_('Phone 1'), max_length=9, null=True,
                             blank=True, help_text=_('9 digits maximum'))
    phone_alt = models.CharField(_('Phone 2'), max_length=9, null=True,
                             blank=True, help_text=_('9 digits maximum'))

    nid = models.CharField(_('Identification document'), max_length=200,
                           null=True, blank=True)
    
    website = models.URLField(_('Website'), max_length=200,
                              null=True, blank=True)
    spaces = models.ManyToManyField(Space)
    interests = models.ManyToManyField(Interest, blank=True, null=True)
    
    # Not required since User module automatically sets the register time.
    #registered = models.DateTimeField('Registered', auto_now_add=True)

    def get_age(self):
        
        """
        Get the current user age.
        """

        if self.birthdate is not None:
            diff = datetime.date.today() - self.birthdate
            years = diff.days/365
            return years
        else:
            return '??'

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
