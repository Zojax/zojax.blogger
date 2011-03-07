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
from zojax.blogger.interfaces import _

from zojax.content.discussion.interfaces import IRecentCommentsPortlet
from zojax.widget.radio.field import RadioChoice


class IBlogPortlet(interface.Interface):
    """ Blog portlet """


class IBlogViewspacePortlet(interface.Interface):
    """ Blog viewspace portlet """


class IBlogArchivePortlet(interface.Interface):
    """ Blog archive portlet """


class IBlogTagsPortlet(interface.Interface):
    """ Blog tags portlet """


class ICategoriesPortlet(interface.Interface):
    """ categories portlet """


class IRecentCommentsPortlet(IRecentCommentsPortlet):
    """ blog recent comments """


class IRecentPostsPortlet(interface.Interface):
    """recent blog posts portlet """

    number = schema.Int(
        title = _(u'Number of posts'),
        description = _(u'Number of posts to display'),
        default = 10,
        required = True)

    spaceMode = RadioChoice(
        title = _(u'Space mode'),
        default = 1,
        vocabulary='zojax.portlets.recent-spacemodes',
        required = True)