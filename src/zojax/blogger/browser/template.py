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
from email.Utils import formataddr

from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds

from zojax.authentication.utils import getPrincipal
from zojax.ownership.interfaces import IOwnership
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.blogger.interfaces import IBloggerProduct, IAdvancedBlogPost
from zojax.blogger.mailin.interfaces import IBloggerDestination


class BlogPostNotificationMail(object):

    def update(self):
        super(BlogPostNotificationMail, self).update()

        blog = self.context
        post = self.contexts[0]
        request = self.request
        self.post = post

        principal = self.getAuthor()

        profile = IPersonalProfile(principal)
        if profile.email:
            author = profile.title
            self.author = author
            self.addHeader(u'From', formataddr((author, profile.email),))
        else:
            self.author = principal.title or principal.id

        self.url = '%s/'%absoluteURL(post, request)
        self.site = getSite()

        self.destination = IBloggerDestination(getUtility(IBloggerProduct))
        if self.destination.enabled:
            self.addHeader(u'To', self.destination.address)
            self.addHeader(u'Reply-To', self.destination.address)
            self.addHeader(
                u'List-Post', u'<mailto:%s>'%self.destination.address)
        else:
            self.addHeader(u'To', formataddr((self.author, profile.email),))

        self.msgId = self.destination.generateMessageId(self.post)

        space = blog.__parent__
        blogurl = absoluteURL(blog, request)

        self.addHeader(u'List-Id', u'%s, %s'%(space.title, blog.title))
        self.addHeader(u'List-Unsubscribe', u'%s/@@notifications'%blogurl)
        self.addHeader(u'List-Subscribe', u'%s/@@notifications'%blogurl)
        self.addHeader(u'List-Archive', u'%s/'%blogurl)

    def text(self):
        if IAdvancedBlogPost.providedBy(self.post):
            text = self.post.full_post_text
        else:
            text = self.post.text.cooked

        if u'src="@@content.attachment/' in text:
            s = u'src="%s/@@content.attachment/'%absoluteURL(
                getSite(), self.request)
            text = text.replace(u'src="@@content.attachment/', s)

        return text

    def getAuthor(self):
        post = self.contexts[0]
        return IOwnership(post).owner

    @property
    def subject(self):
        return u'%s: %s'%(self.context.title, self.post.title)

    @property
    def messageId(self):
        return self.msgId


class BlogPostCommentNotificationMail(BlogPostNotificationMail):

    def update(self):
        super(BlogPostCommentNotificationMail, self).update()

        self.addHeader('In-Reply-To', self.msgId)
        self.comment = self.contexts[1].comment.replace('\n', '<br />')

    def getAuthor(self):
        comment = self.contexts[1]
        return getPrincipal(comment.author)

    @property
    def messageId(self):
        return self.destination.generateMessageId(self.post, self.contexts[1])
