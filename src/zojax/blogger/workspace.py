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
from zojax.content.space.interfaces import IContentSpace
from zojax.content.space.workspace import WorkspaceFactory

from blog import BaseBlog
from interfaces import _, IBloggerWorkspace, ISpaceBloggerWorkspaceFactory


class BloggerWorkspace(BaseBlog):
    interface.implements(IBloggerWorkspace)

    @property
    def space(self):
        return self.__parent__


class BloggerWorkspaceFactory(WorkspaceFactory):
    component.adapts(IContentSpace)
    interface.implements(ISpaceBloggerWorkspaceFactory)

    name = 'blog'
    title = _(u'Blog')
    description = _(u'Space blog.')
    weight = 1000

    factory = BloggerWorkspace
