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
import rwproperty
from zope import interface, component
from zope.schema.fieldproperty import FieldProperty
from zope.dublincore.interfaces import IDCPublishing
from zojax.richtext.field import RichTextProperty
from zojax.content.type.item import PersistentItem
from zojax.content.type.searchable import ContentSearchableText

from interfaces import IBlogPost


class BlogPost(PersistentItem):
    interface.implements(IBlogPost)

    text = RichTextProperty(IBlogPost['text'])
    abstract = RichTextProperty(IBlogPost['abstract'])
    category = FieldProperty(IBlogPost['category'])

    @rwproperty.getproperty
    def date(self):
        return self.__dict__.get('date', None)

    @rwproperty.setproperty
    def date(self, value):
        publishing = IDCPublishing(self)
        publishing.effective = value
        self.__dict__['date'] = publishing.effective
        self._p_changed = True


class PostSearchableText(ContentSearchableText):
    component.adapts(IBlogPost)

    def getSearchableText(self):
        text = super(PostSearchableText, self).getSearchableText()
        try:
            return text + u' ' + self.content.text.text
        except AttributeError:
            return text
