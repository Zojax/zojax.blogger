##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""

import pytz
from datetime import datetime
from rwproperty import setproperty, getproperty

from zope import interface, component
from zope.dublincore.interfaces import IDCPublishing
from zope.location import LocationProxy
from zope.publisher.interfaces import IPublishTraverse, NotFound, Unauthorized
from zope.schema.fieldproperty import FieldProperty

from zojax.content.forms.content import ContentStep
from zojax.content.forms.interfaces import IEditContentWizard
from zojax.content.forms.wizardedit import EditContentWizard
from zojax.content.type.item import PersistentItem
from zojax.content.type.searchable import ContentSearchableText
from zojax.filefield.field import FileFieldProperty
from zojax.resourcepackage.library import include
from zojax.richtext.field import RichTextProperty
from zojax.wizard.interfaces import ISaveable

from interfaces import IBlogPost, IAdvancedBlogPost


class BlogPost(PersistentItem):
    interface.implements(IBlogPost)

    text = RichTextProperty(IBlogPost['text'])
    abstract = RichTextProperty(IBlogPost['abstract'])
    image = FileFieldProperty(IBlogPost['image'])
    category = FieldProperty(IBlogPost['category'])

    @getproperty
    def published(self):
        return self.__dict__.get('published', None)

    @setproperty
    def published(self, value):
        self.__dict__['published'] = value
        self._p_changed = True

    @getproperty
    def date(self):
        return self.__dict__.get('date', None)

    @setproperty
    def date(self, value):
        publishing = IDCPublishing(self)
        publishing.effective = value
        self.__dict__['date'] = publishing.effective
        if datetime.now(pytz.utc) >= self.date:
            self.__dict__['published'] = True
        else:
            self.__dict__['published'] = False
        self._p_changed = True


class AdvancedBlogPost(BlogPost):
    interface.implements(IAdvancedBlogPost)

    @getproperty
    def pages(self):
        return self.__dict__.get('pages', [])

    @setproperty
    def pages(self, value):
        old = self.pages
        if value is not None:
            if len(value) > len(old):
                old.extend(value[len(old):])
            else:
                old = old[:len(value)]
        else:
            self.__data__['pages'] = []
            return
        for k, v in enumerate(value):
            ov = old[k]
            if v.text:
                ov.text = v.text
            else:
                ov.text = u''
            ov.position = v.position

        # NOTE: sort by position
        old = sorted(old, key=lambda x: x.position)
        self.__dict__['pages'] = old

    @property
    def text(self):
        return ''.join(
            [getattr(page.text, 'cooked', '') for page in self.pages])


class PostSearchableText(ContentSearchableText):
    component.adapts(IBlogPost)

    def getSearchableText(self):
        text = super(PostSearchableText, self).getSearchableText()
        try:
            return text + u' ' + self.content.text.text
        except AttributeError:
            return text


class AdvancedBlogPostSearchableText(ContentSearchableText):
    component.adapts(IAdvancedBlogPost)

    def getSearchableText(self):
        text = super(AdvancedBlogPostSearchableText, self).getSearchableText()
        try:
            return text + u' ' + self.content.text
        except AttributeError:
            return text


class Pages(object):

    interface.implements(IPublishTraverse)

    __name__ = 'pages'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        context = self.context
        try:
            return LocationProxy(
                context.pages[int(name) - 1], self.context, name)
        except ValueError, e:
            # 403 error
            raise Unauthorized("Access to images folder denied")
        except IndexError, e:
            # 404 error
            raise NotFound(self.context, self.__name__, request)
        except TypeError, e:
            raise

        raise NotFound(self.context, self.__name__, request)


class AdvancedBlogPostEditForm(EditContentWizard):
    interface.implements(ISaveable, IEditContentWizard)

    def __init__(self, *args, **kw):
        include('blogger-advanced-post-form-js')
        super(AdvancedBlogPostEditForm, self).__init__(*args, **kw)


class AdvancedBlogPostAddForm(ContentStep):
    interface.implements(ISaveable)

    def __init__(self, *args, **kw):
        include('blogger-advanced-post-form-js')
        super(AdvancedBlogPostAddForm, self).__init__(*args, **kw)
