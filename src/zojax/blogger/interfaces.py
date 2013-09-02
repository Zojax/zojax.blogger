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
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from zojax.richtext.field import RichText
from zojax.widget.checkbox.field import CheckboxList
from zojax.content.feeds.interfaces import IRSS2Feed
from zojax.content.type.interfaces import IItem, IContent
from zojax.content.space.interfaces import IWorkspace, IWorkspaceFactory
from zojax.content.notifications.interfaces import IContentNotification
from zojax.security.interfaces import IPermissionCategory

_ = MessageFactory('zojax.blogger')


class IBlog(IItem):
    """ Blog """

    dates = interface.Attribute('Dates')
    index = interface.Attribute('Primary index')

    pageSize = schema.Int(
        title = _(u'Page size'),
        description = _(u'Number of entries per page.'),
        default = 10)

    def entries():
        """List entries names."""


class IBlogPostListing(interface.Interface):
    """Blog post listing"""

    def update(post):
        """Update post index."""

    def remove(post, name):
        """Remove post from index."""


class IBlogPost(interface.Interface):
    """ Blog post """

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Post title.'),
        default = u'',
        missing_value = u'',
        required = True)

    text = RichText(
        title = _(u'Text'),
        description = _(u'Blog post body text.'),
        required = True)

    abstract = RichText(
        title = _(u'Abstract'),
        description = _(u'Blog post abstract text.'),
        required = True)

    date = schema.Datetime(
        title = _('Publish Date / Time'),
        description = _('Post date.'),
        required = True)

    category = CheckboxList(
        title = _(u'Category'),
        description = _('Select category for blog post.'),
        vocabulary = 'zojax.blogger-categories',
        default = [],
        required = False)

    published = schema.Bool(
        title=_(u'Published'),
        default=None,
        required=False
    )


class IBlogPostType(interface.Interface):
    """ Blog post content type """


class ICategory(IItem):
    """ Entries Category """


class ICategoryContainer(interface.Interface):
    """ Categories container """


class IBloggerProduct(interface.Interface):
    """ product """

    usePostAbstractField = schema.Bool(
        title = _(u'Use post abstract field'),
        description = _(u'Use post abstract field on post view.'),
        default = False)


class IBlogPostView(interface.Interface):
    """ Blog post view """


class IYear(IContent):
    """ interface for year """


class IMonth(IContent):
    """ interface for month """


class IBlogTags(interface.Interface):
    """ blog tags """

    engine = interface.Attribute('Tags engine')

    def hasTag(tag):
        """ """

    def listTags(post):
        """Return list of tags"""


class IBlogTagsManager(interface.Interface):
    """ manage blog tags """

    def update(post):
        """Update tags for post."""

    def remove(post):
        """Remove tags for post."""


class IBloggerWorkspace(IBlog, IWorkspace):
    """ blogger workspace """


class IBloggerWorkspaceFactory(IWorkspaceFactory):
    """ blogger workspace factory """


class ISpaceBloggerWorkspaceFactory(IBloggerWorkspaceFactory):
    """ blogger workspace factory """


class IBlogPostsRSSFeed(IRSS2Feed):
    """ blog posts rss feed """


class IBlogNotification(IContentNotification):
    """ blog notification """


class IBloggerPermissions(IPermissionCategory):
    """ blog permissions """


class IBlogPostPage(interface.Interface):

    text = RichText(
        title = _(u'Text'),
        description = _(u'Blog post body text.'),
        required = True)

    position = schema.TextLine(
        title=_(u'Position'),
        required=False)


class IAdvancedBlogPost(interface.Interface):
    """ Advanced Blog post """

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Post title.'),
        default = u'',
        missing_value = u'',
        required = True)

    abstract = RichText(
        title = _(u'Abstract'),
        description = _(u'Blog post abstract text.'),
        required = True)

    date = schema.Datetime(
        title = _('Publish Date / Time'),
        description = _('Post date.'),
        required = True)

    category = CheckboxList(
        title = _(u'Category'),
        description = _('Select category for blog post.'),
        vocabulary = 'zojax.blogger-categories',
        default = [],
        required = False)

    published = schema.Bool(
        title=_(u'Published'),
        default=None,
        required=False
    )

    pages = schema.List(
        title=_(u"Pages"),
        value_type=schema.Object(
            title=_(u'page'),
            schema=IBlogPostPage),
        default=[],
        required=False)


class IAdvancedBlogPostType(interface.Interface):
    """ Blog post content type """
    pages = schema.List(
        title=_(u"Pages"),
        value_type=schema.Object(
            title=_(u'page'),
            schema=IBlogPostPage),
        default=[],
        required=False)

