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
from zope.proxy import removeAllProxies
from zope.traversing.browser import absoluteURL

from zojax.blogger.interfaces import IBlog
from zojax.content.space.interfaces import ISpace


class BlogTagsPortlet(object):

    blog = False

    def update(self):
        context = self.context
        while not ISpace.providedBy(context):
            context = context.__parent__

        try:
            blog = context.get('blog')
            if not IBlog.providedBy(blog):
                return
        except:
            return

        self.blog = True
        self.context = blog
        self.blog_url = absoluteURL(removeAllProxies(blog), self.request)

        super(BlogTagsPortlet, self).update()

    def listTags(self):
        tags = []
        engine = removeAllProxies(self.context['tags'].engine)
        for weight, tag in engine.getTagCloud():
            tags.append({'tag': tag, 'weight': weight+100})

        return tags

    def isAvailable(self):
        return self.blog and self.context['tags']
