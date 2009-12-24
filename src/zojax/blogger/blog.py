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
import time, datetime
from BTrees.OOBTree import OOSet
from BTrees.IOBTree import IOBTree
from BTrees.IFBTree import IFBTree, weightedIntersection

from zope import interface, event, component
from zope.component import getUtility
from zope.proxy import removeAllProxies, sameProxiedObjects
from zope.app.intid.interfaces import IIntIds
from zope.app.intid.interfaces import IIntIdAddedEvent
from zope.app.intid.interfaces import IIntIdRemovedEvent
from zope.schema.fieldproperty import FieldProperty
from zope.security.proxy import removeSecurityProxy
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.copypastemove.interfaces import IObjectMover
from zope.app.container.contained import NameChooser
from zope.app.container.interfaces import IObjectMovedEvent

from zojax.catalog.interfaces import ICatalog
from zojax.content.type.container import ContentContainer

from date import Year
from tags import BlogTags
from category import CategoryContainer
from interfaces import IBlog, IBlogPost, IBlogPostListing


class BaseBlog(ContentContainer):
    interface.implements(IBlog, IBlogPostListing)

    pageSize = FieldProperty(IBlog['pageSize'])

    def __init__(self, *args, **kw):
        super(BaseBlog, self).__init__(*args, **kw)

        self.dates = OOSet()
        self.index = IFBTree()

    def entries(self, index=None):
        if index is None:
            result = self.index
        else:
            _t, result = weightedIntersection(index, self.index)

        return result.byValue(0)

    def update(self, post):
        uid = getUtility(IIntIds).getId(post)
        if uid in self.index:
            self.remove(post)

        date = post.date.timetuple()
        idx = time.mktime(date)
        self.index[uid] = idx

        # update in dates
        yearName = str(date[0])
        year = self.get(yearName)
        if year is None:
            year = Year()
            event.notify(ObjectCreatedEvent(year))
            self[yearName] = year
            self.dates.insert(yearName)

        year.update(date, uid, idx)

        # update categories
        self['category'].update(post, uid, idx)

        # update tags info
        self['tags'].update(post, uid)

    def remove(self, post):
        uid = getUtility(IIntIds).getId(post)
        if uid not in self.index:
            return

        date = time.localtime(self.index[uid])

        # remove from dates
        yearName = str(date[0])
        year = self.get(yearName)
        if year is not None:
            year.remove(date, uid)
            if not len(year):
                if yearName in self.dates:
                    self.dates.remove(yearName)

                del self[yearName]

        # remove from category
        self['category'].remove(uid)

        # remove tags info
        self['tags'].remove(post, uid)

        # remove from index
        del self.index[uid]


@component.adapter(IBlog, IIntIdAddedEvent)
def blogAdded(object, obevent):
    if u'category' not in object:
        category = CategoryContainer()
        event.notify(ObjectCreatedEvent(category))
        object[u'category'] = category

    if u'tags' not in object:
        tags = BlogTags()
        event.notify(ObjectCreatedEvent(tags))
        object[u'tags'] = tags


@component.adapter(IBlogPost, IObjectMovedEvent)
def blogPostMoved(post, event):
    id = getUtility(IIntIds).queryId(removeAllProxies(post))
    if id is None:
        return

    if IBlog.providedBy(event.oldParent):
        removeSecurityProxy(event.oldParent).remove(post)

    if IBlog.providedBy(event.newParent):
        removeSecurityProxy(event.newParent).update(post)


@component.adapter(IBlogPost, IIntIdRemovedEvent)
def blogPostRemoved(post, event):
    if not sameProxiedObjects(post, event.original_event.object):
        return

    if IBlog.providedBy(post.__parent__):
        removeSecurityProxy(post.__parent__).remove(post)


@component.adapter(IBlogPost, IObjectModifiedEvent)
def blogPostModified(post, event):
    post = removeAllProxies(post)

    blog = post.__parent__
    if IBlog.providedBy(blog):
        blog.update(post)
