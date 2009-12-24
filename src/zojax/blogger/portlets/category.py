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
from zojax.cache.view import cache
from zojax.cache.keys import ContextModified


class CategoriesPortlet(object):

    categories = ()

    def __init__(self, context, request, view, manager):
        context = context['category']

        super(CategoriesPortlet, self).__init__(context, request, view, manager)

    def update(self):
        context = self.context

        categories = []
        for category in context.values():
            categories.append((category.title, category.__name__))

        categories.sort()
        self.categories = [{'name':name, 'title':title}
                           for title, name in categories]

    def isAvailable(self):
        return bool(self.categories)

    @cache('portlets.blogger.categories', ContextModified)
    def updateAndRender(self):
        return super(CategoriesPortlet, self).updateAndRender()
