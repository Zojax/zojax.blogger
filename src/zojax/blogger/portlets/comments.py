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
from zojax.blogger.interfaces import IBlog
from zojax.content.discussion.portlet import RecentCommentsPortlet


class BlogRecentCommentsPortlet(RecentCommentsPortlet):

    blog = False

    def __init__(self, context, request, manager, view):
        super(BlogRecentCommentsPortlet, self).__init__(
            context, request, manager, view)

        blog = context.get('blog')
        if not IBlog.providedBy(blog):
            return

        self.blog = True
        self.context = blog

    def isAvailable(self):
        return self.blog and bool(self.comments)
