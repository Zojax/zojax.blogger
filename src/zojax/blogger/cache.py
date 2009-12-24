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
from zope import component

from zojax.cache.tag import ContextTag
from zojax.content.type.interfaces import IDraftedContent
from zojax.content.discussion.interfaces import ICommentEvent

from interfaces import IBlogPost


BloggerPosts = ContextTag('blogger.posts')
BloggerComments = ContextTag('blogger.discussion')


def blogPostHandler(post, event):
    if not IDraftedContent.providedBy(post):
        BloggerPosts.update(post)


@component.adapter(IBlogPost, ICommentEvent)
def commentsHandler(post, event):
    BloggerComments.update(post)
