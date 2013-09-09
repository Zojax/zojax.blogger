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

from rwproperty import setproperty, getproperty

from zope import interface, component
from datetime import datetime
import pytz
from zope.location import LocationProxy
from zope.publisher.interfaces import IPublishTraverse, NotFound, Unauthorized
from zope.schema.fieldproperty import FieldProperty
from zope.dublincore.interfaces import IDCPublishing
from zojax.richtext.field import RichTextProperty
from zojax.content.type.item import PersistentItem
from zojax.content.type.searchable import ContentSearchableText

from interfaces import IBlogPost, IAdvancedBlogPost


class BlogPost(PersistentItem):
    interface.implements(IBlogPost)

    text = RichTextProperty(IBlogPost['text'])
    abstract = RichTextProperty(IBlogPost['abstract'])
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
        if datetime.now(pytz.utc)>=self.date:
            self.__dict__['published']=True
        else:
            self.__dict__['published']=False
        self._p_changed = True


class AdvancedBlogPost(BlogPost):
    interface.implements(IAdvancedBlogPost)

    @getproperty
    def text(self):
        return self.__dict__.get('text', [])

    @setproperty
    def text(self, value):
        old = self.text
        if value is not None:
            if len(value) > len(old):
                old.extend(value[len(old):])
            else:
                old = old[:len(value)]
        else:
            self.__data__['text'] = []
            return
        for k, v in enumerate(value):
            ov = old[k]
            if v.text:
                ov.text = v.text
            ov.position = v.position

        # NOTE: sort by position
        old = sorted(old, key=lambda x: x.position)
        self.__dict__['text'] = old

    @property
    def full_post_text(self):
        return ''.join([getattr(page.text, 'cooked', '') for page in self.text])


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
            return text + u' ' + self.content.full_post_text
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
        # import ipdb; ipdb.set_trace()
        try:
            return LocationProxy(context.pages[int(name)-1], self.context, name)
        except ValueError, e:
            # 403 error
            raise Unauthorized("Access to images folder denied")
        except IndexError, e:
            # 404 error
            raise NotFound(self.context, self.__name__, request)
        except TypeError, e:
            raise

        raise NotFound(self.context, self.__name__, request)
