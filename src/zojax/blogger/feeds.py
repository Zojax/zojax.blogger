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
import time, rfc822
from zope import component, interface
from zope.component import getUtility
from zope.traversing.browser import absoluteURL

from zojax.content.feeds.rss2 import RSS2Feed
from zojax.catalog.interfaces import ICatalog
from zojax.ownership.interfaces import IOwnership
from zojax.content.space.interfaces import ISpace
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.content.discussion.feeds import CommentsFeed

from interfaces import _, IBlog, IBlogPostsRSSFeed


class BlogCommentsFeed(CommentsFeed):
    component.adapts(IBlog)

    title = _(u'Recent comments')
    description = _(u'Blog recent comments.')

    def getContext(self):
        context = self.context
        while not ISpace.providedBy(context):
            context = context.__parent__
            if context is None:
                return

        try:
            blog = context.get('blog')
            if not IBlog.providedBy(blog):
                return
        except:
            return

        return blog


class BlogPostsRSSFeed(RSS2Feed):
    component.adapts(ISpace)
    interface.implementsOnly(IBlogPostsRSSFeed)

    name = 'blogposts'
    title = _(u'Blog posts')
    description = _(u'Recent blog posts.')

    def items(self):
        request = self.request
        catalog = getUtility(ICatalog)

        results = getUtility(ICatalog).searchResults(
            traversablePath={'any_of':(self.context,)},
            type={'any_of': ('content.blogpost',)},
            sort_order='reverse', sort_on='effective',
            isDraft={'any_of': (False,)})

        for item in results:
            url = absoluteURL(item, request)

            info = {
                'title': u'%s in %s'%(item.title, item.__parent__.title),
                'description': item.text.cooked,
                'guid': '%s/'%url,
                'pubDate': rfc822.formatdate(time.mktime(item.date.timetuple())),
                'isPermaLink': True}

            principal = IOwnership(item).owner
            if principal is not None:
                profile = IPersonalProfile(principal)
                info['author'] = u'%s (%s)'%(profile.email, profile.title)

            yield info
