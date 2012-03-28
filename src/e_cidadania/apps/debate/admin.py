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

from django.contrib import admin

from e_cidadania.apps.debate.models import Debate, Note, Column, Row

class ColumnInline(admin.TabularInline):

    """
    """
    model = Column
    extra = 2
    
class RowInline(admin.TabularInline):

    """
    """
    model = Row
    extra = 2

class DebateAdmin(admin.ModelAdmin):
    
    """
    Administration for all the debates.
    """
    list_display = ('title', 'date')
    inlines = [ColumnInline, RowInline]
    
    
class NoteAdmin(admin.ModelAdmin):
    
    """
    Administration for all the notes in every debate.
    """
    list_display = ('message', 'date', 'author')

admin.site.register(Debate, DebateAdmin)
admin.site.register(Note, NoteAdmin)
