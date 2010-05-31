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
from persistent import Persistent

from zope import interface, component
from zope.location import Location
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds
from zope.app.container.contained import Contained
from zope.publisher.interfaces import NotFound
from zope.dublincore.interfaces import ICMFDublinCore
from zope.security.proxy import removeSecurityProxy
from zojax.tagging.engine import TaggingEngine

from interfaces import IBlogTags, IBlogTagsManager


class BlogTags(Persistent, Contained):
    interface.implements(IBlogTags, IBlogTagsManager)

    def __init__(self):
        self.engine = TaggingEngine()

    def __nonzero__(self):
        return self.engine.tagsCount > 0

    def update(self, post, uid):
        tags = self._normalize(ICMFDublinCore(post).Subject())
        self.engine.update(uid, tags)

    def remove(self, post, uid):
        self.engine.remove(uid)

    def _normalize(self, contenttags):
        tags = []

        for tag in contenttags:
            tag = tag.lower().strip()
            if tag:
                tags.append(tag)

        return tags

    def hasTag(self, tag):
        return tag in self.engine

    def listTags(self, post):
        return [tag for weight, tag in self.engine.getItemsTagCloud(
                (getUtility(IIntIds).getId(removeSecurityProxy(post)),))]


class BlogTag(Location):

    def __init__(self, context, request, tag):
        self.context = context
        self.request = request
        self.tag = tag

        self.__name__ = tag
        self.__parent__ = context

    def entries(self):
        blog = self.context.__parent__
        items = removeAllProxies(self.context.engine).getItems((self.tag,))
        return blog.entries(items)


class BlogTagsPublisher(object):
    component.adapts(IBlogTags, interface.Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def publishTraverse(self, request, name):
        if self.context.hasTag(name):
            return BlogTag(self.context, request, name)

        raise NotFound(self.context, name, request)
