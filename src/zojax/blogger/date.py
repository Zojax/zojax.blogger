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

from zope import event, interface
from zope.lifecycleevent import ObjectCreatedEvent
from zojax.content.type.item import PersistentItem
from zojax.content.type.container import BaseContentContainer

from interfaces import IYear, IMonth


class Year(BaseContentContainer):
    interface.implements(IYear)

    def __init__(self, *args, **kw):
        super(Year, self).__init__(*args, **kw)

        self.index = IFBTree()

    @property
    def title(self):
        return self.__name__

    @property
    def description(self):
        return u''

    def entries(self):
        return self.__parent__.entries(self.index)

    def update(self, date, uid, idx):
        if uid in self.index:
            self.remove(date, uid)

        self.index[uid] = idx

        mid = str(date[1])
        month = self.get(mid)
        if month is None:
            month = Month()
            event.notify(ObjectCreatedEvent(month))
            self[mid] = month

        month.update(uid, idx)

    def remove(self, date, uid):
        if uid in self.index:
            del self.index[uid]

        mid = str(date[1])
        month = self.get(mid)
        if month is not None:
            month.remove(uid)
            if not month:
                del self[mid]


class Month(PersistentItem):
    interface.implements(IMonth)

    def __init__(self, *args, **kw):
        super(Month, self).__init__(*args, **kw)

        self.index = IFBTree()

    @property
    def title(self):
        return self.__name__

    @property
    def description(self):
        return u''

    def entries(self):
        return self.__parent__.__parent__.entries(self.index)

    def update(self, uid, idx):
        self.index[uid] = idx

    def remove(self, uid):
        if uid in self.index:
            del self.index[uid]

    def __nonzero__(self):
        return bool(self.index)
