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

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from e_cidadania.apps.spaces.file_validation import ContentTypeRestrictedFileField
from fields import StdImageField

ALLOWED_CONTENT_TYPES = [
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/pdf',
    'application/msword',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.oasis.opendocument.presentation',
    'application/vnd.oasis.opendocument.spreadsheet',
    'application/vnd.openofficeorg.extension',
]

class Space(models.Model):

    """     
    Spaces model. This model stores a "space" or "place" also known as a
    participative process in reality. Every place has a minimum set of
    settings for customization.
    """
    name = models.CharField(_('Name'), max_length=250, unique=True,
                            help_text=_('Max: 250 characters'))
    url = models.CharField(_('URL'), max_length=100, unique=True,
                            validators=[RegexValidator(
                                        regex='^[a-z0-9_]+$',
                                        message='Invalid characters in the space URL.'
                                       )],
                            help_text=_('Valid characters are lowercase, digits and \
                                         underscore. This will be the accesible URL'))
    description = models.TextField(_('Description'),
                                    default=_('Write here your description.'))
    date = models.DateTimeField(_('Date of creation'), auto_now_add=True)
    author = models.ForeignKey(User, blank=True, null=True,
                                verbose_name=_('Space creator'))

    logo = StdImageField(upload_to='spaces/logos', size=(100, 75, False), 
                         help_text = _('Valid extensions are jpg, jpeg, png and gif'))
    banner = StdImageField(upload_to='spaces/banners', size=(500, 75, False),
                           help_text = _('Valid extensions are jpg, jpeg, png and gif'))
#    logo = models.ImageField(upload_to='spaces/logos',
#                             verbose_name=_('Logotype'),
#                             help_text=_('100x75 pixels'))
#    banner = models.ImageField(upload_to='spaces/banners',
#                               verbose_name=_('Banner'),
#                               help_text=_('75px height'))
    public = models.BooleanField(_('Public space'))
    #theme = models.CharField(_('Theme'), m)
    
    # Modules
    mod_debate = models.BooleanField(_('Debate'))
    mod_proposals = models.BooleanField(_('Proposals'))
    mod_news = models.BooleanField(_('News'))
    mod_cal = models.BooleanField(_('Calendar'))
    mod_docs = models.BooleanField(_('Documents'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Space')
        verbose_name_plural = _('Spaces')
        get_latest_by = 'date'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('space-index', (), {
            'space_name': self.url})


class Entity(models.Model):

    """
    This model stores the name of the entities responsible for the creation
    of the space or supporting it.
    """
    name = models.CharField(_('Name'), max_length=100, unique=True)
    website = models.CharField(_('Website'), max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='spaces/logos', verbose_name=_('Logo'),
                             blank = True, null = True)
    space = models.ForeignKey(Space, blank=True, null=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Entity')
        verbose_name_plural = _('Entities')

    def __unicode__(self):
        return self.name

        
class Document(models.Model):

    """
    This models stores documents for the space, like a document repository,
    There is no restriction in what a user can upload to the space
    """
    title = models.CharField(_('Document title'), max_length=100)
    space = models.ForeignKey(Space, blank=True, null=True)
    docfile = ContentTypeRestrictedFileField(_('File'),
        upload_to='spaces/documents/%Y/%m/%d',
        content_types=ALLOWED_CONTENT_TYPES,
        max_upload_size=26214400
    )
    #docfile = models.FileField(upload_to='spaces/documents/%Y/%m/%d')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name=_('Author'), blank=True,
                               null=True)
    
    def get_file_ext(self):
        filename = self.docfile.name
        extension = filename.split('.')
        return extension[1].upper()

    def get_file_size(self):
        if self.docfile.size < 1023:
            return str(self.docfile.size) + " Bytes"
        elif self.docfile.size >= 1024 and self.docfile.size <= 1048575:
            return str(round(self.docfile.size / 1024.0, 2)) + " KB"
        elif self.docfile.size >= 1048576:
            return str(round(self.docfile.size / 1024000.0, 2)) + " MB"
        
    class Meta:
        ordering = ['pub_date']
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        get_latest_by = 'pub_date'
    
    # There is no 'view-document' view, so I'll leave the get_absolute_url
    # method without permalink. Remember that the document files are accesed
    # through the url() method in templates.
    def get_absolute_url(self):
        return '/spaces/%s/docs/%s' % (self.space.url, self.id)

class Event(models.Model):

    """
    Meeting data model. Every space (process) has N meetings. This will
    keep record of the assistants, meeting name, etc.
    """
    title = models.CharField(_('Event name'), max_length=100)
    space = models.ForeignKey(Space, blank=True, null=True)
    user = models.ManyToManyField(User, verbose_name=_('Users'))
    pub_date = models.DateTimeField(auto_now_add=True)
    event_author = models.ForeignKey(User, verbose_name=_('Created by'),
                                     blank=True, null=True,
                                     related_name='meeting_author')
    event_date = models.DateField(verbose_name=_('Event date'))
    description = models.TextField(_('Description'), blank=True, null=True)
    location = models.TextField(_('Location'), blank=True, null=True)
    
    class Meta:
        ordering = ['event_date']
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        get_latest_by = 'event_date'

    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('view-event', (), {
            'space_name': self.space.url,
            'event_id': str(self.id)})
