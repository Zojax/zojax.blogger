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
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds
from zope.traversing.browser import absoluteURL

from zojax.batching.batch import Batch
from zojax.blogger.interfaces import IBlog


class TagView(object):

    def update(self):
        context = self.context

        blog = context.__parent__.__parent__

        self.blog = blog
        self.batch = Batch(
            context.entries(), size=blog.pageSize,
            context=context, request=self.request)

        self.ids = getUtility(IIntIds)

    def getPost(self, idx):
        return self.ids.getObject(idx[1])



class TagsView(object):

    def __call__(self, *args, **kw):
        request = self.request
        request.response.redirect(
            '%s/'%absoluteURL(self.context.__parent__, request))
