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
from zope import interface, component
from zope.security import checkPermission
from zope.traversing.browser import absoluteURL

from zojax.blogger.interfaces import _, IBlog, IBlogPost
from zojax.personal.content.interfaces import IContentWorkspace
from zojax.content.actions.interfaces import IAddContentCategory
from zojax.content.actions.contentactions import EditContentAction,ContentAction

import interfaces


class WritePostAction(ContentAction):
    interface.implements(interfaces.IWritePostAction, IAddContentCategory)

    weight = 100
    title = _(u'Create Blog post')
    contextInterface = IBlog

    @property
    def url(self):
        return '%s/+/content.blogpost/'%(absoluteURL(self.context,self.request))

    def isAvailable(self):
        return checkPermission('zojax.AddBlogPost', self.context) or \
               checkPermission('zojax.SubmitBlogPost', self.context)


class ManageBlogAction(EditContentAction):
    component.adapts(IBlogPost, interface.Interface)
    interface.implements(interfaces.IManageBlogAction)

    weight = 200
    title = _(u'Manage blog')
    contextInterface = IBlog


class BlogRSSFeedAction(object):
    component.adapts(IBlog, interface.Interface)
    interface.implements(interfaces.IBlogRSSFeedAction)

    weight = 99999
    title = _(u'RSS Feed')
    description = u''

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def url(self):
        return '%s/@@feeds/blogposts'%absoluteURL(self.context, self.request)

    def isAvailable(self):
        return True
