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
from zope.app.intid.interfaces import IIntIdAddedEvent
from zojax.subscription.interfaces import ISubscriptionDescription
from zojax.content.draft.interfaces import IDraftPublishedEvent
from zojax.content.discussion.interfaces import ICommentAddedEvent
from zojax.content.notifications.utils import sendNotification
from zojax.content.notifications.notification import Notification

from interfaces import _, IBlogPost, IBloggerWorkspace, IBlogNotification


class BloggerNotification(Notification):
    component.adapts(IBloggerWorkspace)
    interface.implementsOnly(IBlogNotification)

    type = u'blog'
    title = _(u'Blog')
    description = _(u'Recently added blog posts.')


class BloggerNotificationDescription(object):
    interface.implements(ISubscriptionDescription)

    title = _(u'Blog')
    description = _(u'Recently added blog posts.')


@component.adapter(IBlogPost, IDraftPublishedEvent)
def blogPostPublished(post, ev):
    sendNotification('blog', post.__parent__, post)


@component.adapter(IBlogPost, ICommentAddedEvent)
def commentAdded(post, ev):
    sendNotification('blog', post.__parent__, post, ev.comment)
