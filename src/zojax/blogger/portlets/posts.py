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
from zope import interface
from zope.component import getUtility, getMultiAdapter
from zojax.catalog.interfaces import ICatalog
from zojax.content.space.portlets.content import RecentContentPortlet

from zojax.cache.view import cache
from zojax.cache.timekey import TagTimeKey, each5minutes, each15minutes
from zojax.cache.interfaces import IVisibleContext

from zojax.portlet.cache import PortletId, PortletModificationTag

from zojax.blogger.cache import BloggerPosts, BloggerComments
from zojax.blogger.interfaces import IBloggerProduct, IBlogPostView

from interfaces import IRecentPostsPortlet

def BlogPostsKey(object, instance, *args, **kw):
    if IVisibleContext.providedBy(instance.context):
        return {'announce': instance.announce}
    else:
        return {'announce': instance.announce,
                'principal': instance.request.principal.id}


class RecentPostsPortlet(RecentContentPortlet):

    rssfeed = 'blogposts'
    cssclass = 'portlet-blogger-posts'

    def __init__(self, context, request, view, manager):
        super(RecentPostsPortlet, self).__init__(context,request,view,manager)

        self.announce = getUtility(IBloggerProduct).usePostAbstractField

    def extraParameters(self):
        return {'sort_on': 'effective',
                'noPublishing': True, 'type': {'any_of': ('content.blogpost',)}}

    def getPostView(self, post):
        if self.announce:
            return getMultiAdapter(
                (post, self.request),
                IBlogPostView, 'announce').updateAndRender()
        else:
            return getMultiAdapter(
                (post, self.request), IBlogPostView, 'blog').updateAndRender()

    @cache(PortletId(), PortletModificationTag, BlogPostsKey,
           TagTimeKey(BloggerPosts, each5minutes, 'posts'))
    def updateAndRender(self):
        self.update()
        if not self.isAvailable():
            return u''
        return self.render()


class ContentRecentPostsPortlet(object):

    def __init__(self, context, request, view, manager):
        super(ContentRecentPostsPortlet, self).__init__(
            context, request, view, manager)

        self.announce = getUtility(IBloggerProduct).usePostAbstractField

    def listContents(self):
        request = self.request
        announce = self.announce

        query = {'traversablePath': {'any_of':(self.context,)},
                 'sort_order': 'reverse',
                 'sort_on': 'effective',
                 'isDraft': {'any_of': (False,)},
                 'noPublishing': True,
                 'type': {'any_of': ('content.blogpost',)}}

        for post in getUtility(ICatalog).searchResults(**query)[:self.number]:
            if announce:
                yield getMultiAdapter(
                    (post, request), IBlogPostView,'announce').updateAndRender()
            else:
                yield getMultiAdapter(
                    (post, request), IBlogPostView, 'blog').updateAndRender()

    @cache(PortletId(), PortletModificationTag, BlogPostsKey,
           TagTimeKey(BloggerPosts, each5minutes, 'posts'),
           TagTimeKey(BloggerComments, each15minutes, 'comments'))
    def updateAndRender(self):
        self.update()
        if not self.isAvailable():
            return u''
        return self.render()
