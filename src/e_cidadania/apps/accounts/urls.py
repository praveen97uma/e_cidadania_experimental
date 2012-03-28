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

from django.conf.urls.defaults import *
#from django.contrib.auth.views import *

urlpatterns = patterns('',

    # No longer required, since they were replaced by django-register
    (r'login/$', 'django.contrib.auth.views.login',
                 {'template_name': 'accounts/login.html'}),

    (r'logout/$', 'django.contrib.auth.views.logout',
                  {'template_name': 'accounts/logout.html'}),

    #(r'^/', include('ecidadania.apps.userprofile.urls'))
    #(r'profile/', 'accounts.views.view_profile'),

)
