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
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.security.proxy import removeSecurityProxy
from zope.app.intid.interfaces import IIntIds
from zojax.blogger.interfaces import IBloggerProduct
from zojax.mailin.mailinaware import MailInAwareDestination
from zojax.product.interfaces import IProductUninstalledEvent

from interfaces import IBloggerDestination


class BloggerMailInDestination(MailInAwareDestination):
    interface.implementsOnly(IBloggerDestination)

    def __init__(self):
        pass

    @property
    def context(self):
        return getUtility(IBloggerProduct)

    def generateMessageId(self, post, salt=None):
        ids = getUtility(IIntIds)
        post = ids.getId(removeAllProxies(post))
        if salt:
            if not isinstance(salt, basestring):
                salt = str(ids.getId(removeAllProxies(salt)))
            return '<%s.%s@zojax.net>'%(post, salt)
        else:
            return '<%s@zojax.net>'%post


@component.adapter(IBloggerProduct)
@interface.implementer(IBloggerDestination)
def getMailInDestination(product):
    product = removeSecurityProxy(product)

    destination = product.data.get('mailin')
    if destination is None:
        destination = BloggerMailInDestination()
        product.data['mailin'] = destination

    return destination


@component.adapter(IProductUninstalledEvent)
def productUninstalled(ev):
    if ev.id == 'blogger':
        IBloggerDestination(ev.product).enabled = False
