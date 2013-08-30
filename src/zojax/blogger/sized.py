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
from zope.size import byteDisplay
from zope.size.interfaces import ISized

from interfaces import IBlog, IBlogPost, IAdvancedBlogPost


class Sized(object):
    component.adapts(IBlogPost)
    interface.implements(ISized)

    def __init__(self, context):
        self.context = context

        self.size = len(context.title) + \
                    len(context.description) + \
                    len(context.text)

    def sizeForSorting(self):
        return "byte", self.size

    def sizeForDisplay(self):
        return byteDisplay(self.size)

class AdvancedBlogSized(object):
    component.adapts(IAdvancedBlogPost)
    interface.implements(ISized)

    def __init__(self, context):
        self.context = context

        self.size = len(context.title) + \
                    len(context.description) + \
                    len(context.text)

    def sizeForSorting(self):
        return "byte", self.size

    def sizeForDisplay(self):
        return byteDisplay(self.size)




class BlogSized(object):
    component.adapts(IBlog)
    interface.implements(ISized)

    def __init__(self, context):
        self.context = context

    def sizeForSorting(self):
        return "post", len(self.context.entries())

    def sizeForDisplay(self):
        return '%s post(s)'%self.sizeForSorting()[1]
