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
from zope import component, interface
from zojax.content.browser.breadcrumb import ContentBreadcrumb
from zojax.blogger.interfaces import IMonth


class MonthBreadcrumb(ContentBreadcrumb):
    component.adapts(IMonth, interface.Interface)

    @property
    def name(self):
        calendar = self.request.locale.dates.calendars['gregorian']
        return calendar.getMonthNames()[int(self.context.__name__)-1]
