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
from zope.component import getUtility, getMultiAdapter
from zope.app.intid.interfaces import IIntIds

from zojax.batching.batch import Batch
from zojax.blogger.interfaces import IBlog, IBlogPostView, IBloggerProduct


class BlogView(object):

    def update(self):
        context = self.context

        blog = context
        while not IBlog.providedBy(blog):
            blog = getattr(blog, '__parent__', None)
            if blog is None:
                return

        self.blog = blog
        self.batch = Batch(
            context.entries(), size=blog.pageSize,
            context=context, request=self.request)

        self.ids = getUtility(IIntIds)
        self.announce = getUtility(IBloggerProduct).usePostAbstractField

    def getPostView(self, idx):
        post = self.ids.getObject(idx[1])

        if self.announce:
            return getMultiAdapter(
                (post, self.request),
                IBlogPostView, 'announce').updateAndRender()
        else:
            return getMultiAdapter(
                (post, self.request), IBlogPostView, 'blog').updateAndRender()


class MonthTitle(object):

    def update(self):
        super(MonthTitle, self).update()

        self.blog = self.context.__parent__.__parent__

        calendar = self.request.locale.dates.calendars['gregorian']
        self.month = u'%s %s'%(
            calendar.getMonthNames()[int(self.context.__name__)-1],
            self.context.__parent__.__name__)
