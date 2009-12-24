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
import pytz
from datetime import datetime
from zope import interface, component, event
from zope.component import getUtility, getAdapter
from zope.security import checkPermission
from zope.security.management import queryInteraction
from zope.app.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent
from zope.interface.common.idatetime import ITZInfo
from zope.lifecycleevent import ObjectModifiedEvent

from zojax.mailin.interfaces import IRecipient
from zojax.mailin.utils import getSubject, getParsedBody
from zojax.richtext.field import RichTextData
from zojax.content.discussion.comment import Comment
from zojax.content.discussion.interfaces import IContentDiscussion
from zojax.content.type.interfaces import IContentType
from zojax.content.draft.interfaces import IDraftContainer, IDraftContentType
from zojax.content.space.interfaces import IWorkspaceFactory
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.blogger.interfaces import IBloggerProduct


class BloggerRecipient(object):
    component.adapts(IBloggerProduct)
    interface.implements(IRecipient)

    def __init__(self, context):
        self.context = context

    def process(self, message):
        title = getSubject(message)
        text = RichTextData(*getParsedBody(message))

        if message.has_key('In-Reply-To'):
            self.reply(title, text, message)
        else:
            self.discussion(title, text, message)

    def reply(self, title, text, message):
        oid = message['In-Reply-To'].split('@', 1)[0].split('.', 1)[0][1:]

        try:
            post = getUtility(IIntIds).getObject(int(oid))
        except:
            return

        if checkPermission('zojax.AddComment', post):
            discussion = IContentDiscussion(post)

            interaction = queryInteraction()
            if interaction is not None and interaction.participations:
                request = interaction.participations[0]

                comment = Comment(request.principal.id, text.text)
                comment.date = datetime.now(ITZInfo(request, pytz.utc))

                comment = discussion.add(comment)
                event.notify(ObjectModifiedEvent(post))

    def discussion(self, title, text, message):
        interaction = queryInteraction()
        if interaction is not None and interaction.participations:
            request = interaction.participations[0]

            space = IPersonalProfile(request.principal).space
            if space is None:
                return

            factory = getAdapter(space, IWorkspaceFactory, 'blog')
            if factory.isAvailable():
                blog = factory.install()

                ct = getUtility(IContentType, 'content.blogpost').__bind__(blog)
                post = ct.add(
                    ct.create(title=title, text=text,
                              date=datetime.now(ITZInfo(request, pytz.utc))))
