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
import urllib
from zope import interface
import re
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from zope.proxy import removeAllProxies
from zope.security import checkPermission
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds
from zope.traversing.browser import absoluteURL
from zope.cachedescriptors.property import Lazy

from zojax.ownership.interfaces import IOwnership
from zojax.content.type.interfaces import IDraftedContent
from zojax.content.forms.content import ContentBasicFields
from zojax.content.discussion.interfaces import IContentDiscussion
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.cache.view import cache
from zojax.cache.keys import ContextModified
from zojax.cache.timekey import TagTimeKey, each10minutes

from zojax.blogger.cache import BloggerComments
from zojax.blogger.interfaces import _, IBlog, IBloggerProduct


class PostContent(ContentBasicFields):

    @Lazy
    def fields(self):
        fields = super(PostContent, self).fields
        fields=fields.omit('published')
        if not getUtility(IBloggerProduct).usePostAbstractField:
            return fields.omit('abstract')
        return fields


class BasePostView(object):

    url = ''
    blog = None
    blog_url = ''
    blog_title = ''
    tags_list = ()
    profile_url = ''
    comments_num = False

    def update(self):
        super(BasePostView, self).update()

        post = removeAllProxies(self.context)
        request = self.request
        owner = IOwnership(post).owner
        profile = IPersonalProfile(owner, None)
        space = getattr(profile, 'space', None)
        profileData = profile.getProfileData()

        self.post = post
        self.postUrl = absoluteURL(post, request)
        self.text = getattr(self.context.text,'cooked','')
        self.biography = profileData.get('about', False)
        self.jobtitle = profileData.get('jobtitle', False)
        if self.biography:
            self.biography = re.sub('<[^>]*>', '', self.biography.text)
            if len(self.biography) >= 240:
                self.biography = self.biography[:240].rsplit(' ', 1)[0].strip() + '...'

        # blog
        if IDraftedContent.providedBy(post):
            blog = post.__parent__
            location = blog.getLocation()
            if location is not None:
                blog = location.get('blog')
            else:
                blog = None
        else:
            blog = post.__parent__

        if IBlog.providedBy(blog):
            self.blog = blog
            self.blog_title = blog.title
            self.blog_url = absoluteURL(blog, request)
            self.tags_list = blog['tags'].listTags(post)

        # author
        try:
            self.author = profile.title
            self.avatar_url = profile.avatarUrl(request)
        except AttributeError:
            self.author = getattr(owner, 'title', '')
            self.avatar_url = '#'

        if space is not None:
            self.profile_url = '%s/profile/'%absoluteURL(space, request)

        # discussion
        discussion = IContentDiscussion(post, None)
        self.comments = discussion is not None and len(discussion)
        self.discussible = discussion is not None and discussion.status != 3
        self.footer_discussion = self.discussible and self.comments_num

        # categories
        categories = []
        ids = getUtility(IIntIds)

        for cId in post.category:
            category = ids.queryObject(cId)
            if category is not None:
                categories.append(
                    (category.title, {'name': category.__name__,
                                      'title': category.title}))

        categories.sort()
        self.categories = [info for t, info in categories]

        self.footer = self.categories or \
            self.tags_list or self.footer_discussion


class PostView(BasePostView):

    @cache('pagelet:blog.post+post', BloggerComments, ContextModified)
    def updateAndRender(self):
        return super(PostView, self).updateAndRender()


class PostBlogView(BasePostView):

    comments_num = True

    def update(self):
        super(PostBlogView, self).update()

        self.url = u'%s/'%absoluteURL(self.post, self.request)

    @cache('pagelet:blog.post+blog', ContextModified,
           TagTimeKey(BloggerComments, each10minutes))
    def updateAndRender(self):
        return super(PostBlogView, self).updateAndRender()


class PostAnnounceView(PostBlogView):

    comments_num = True

    def update(self):
        super(PostAnnounceView, self).update()

        self.url = u'%s/'%absoluteURL(self.post, self.request)

        if getUtility(IBloggerProduct).usePostAbstractField and \
                self.context.abstract is not None:
            self.text = self.context.abstract.cooked

    @cache('pagelet:blog.post+announce', ContextModified,
           TagTimeKey(BloggerComments, each10minutes))
    def updateAndRender(self):
        return super(PostAnnounceView, self).updateAndRender()


class BlogPostView(object):

    def update(self):
        super(BlogPostView, self).update()
        self.draft = IDraftedContent.providedBy(self.context)


class AdvancedBlogPostView(BlogPostView):
    """
    Advanced post view
    """


class AdvancedPostView(PostView):
    """
    Advanced post view
    """
    def update(self):
        super(AdvancedPostView, self).update()
        self.pages = [getattr(p.text, 'cooked', '') for p in self.context.text]
        self.draft = IDraftedContent.providedBy(self.context)