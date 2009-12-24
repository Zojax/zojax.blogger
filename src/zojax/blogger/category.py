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
from BTrees.IFBTree import IFBTree

from zope import interface
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zojax.content.type.item import PersistentItem
from zojax.content.type.container import ContentContainer

from interfaces import ICategory, ICategoryContainer


class Category(PersistentItem):
    interface.implements(ICategory)

    def __init__(self, *args, **kw):
        super(Category, self).__init__(*args, **kw)

        self.index = IFBTree()

    def entries(self):
        return self.__parent__.__parent__.entries(self.index)

    def update(self, uid, idx):
        self.index[uid] = idx

    def remove(self, uid):
        if uid in self.index:
            del self.index[uid]

    def __nonzero__(self):
        return bool(self.index)


class CategoryContainer(ContentContainer):
    interface.implements(ICategoryContainer)

    def update(self, post, uid, idx):
        ids = getUtility(IIntIds)

        for category in self.values():
            category.remove(uid)

            id = ids.getId(category)
            if id in post.category:
                category.update(uid, idx)

    def remove(self, uid):
        for category in self.values():
            category.remove(uid)
