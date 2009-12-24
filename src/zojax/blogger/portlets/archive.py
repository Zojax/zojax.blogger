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
from zope.component import getUtility
from zope.traversing.browser import absoluteURL

from zojax.cache.view import cache
from zojax.cache.keys import ContextModified
from zojax.blogger.interfaces import IBlog
from zojax.catalog.interfaces import ICatalog


class BlogArchivePortlet(object):

    def listDates(self):
        blog = self.context
        request = self.request
        blogurl = absoluteURL(blog, request)
        calendar = request.locale.dates.calendars['gregorian']
        monthNames = calendar.getMonthNames()

        ctool = getUtility(ICatalog)
        contents = ctool.searchResults(searchContext=blog).uids

        dates = []

        for yearName in blog.dates:
            year = blog.get(yearName)
            yearurl = '%s/%s'%(blogurl, yearName)
            if year is not None:
                for mname, month in year.items():
                    posts = month.entries()
                    dates.append(
                        (int(mname),
                         {'url': '%s/%s/'%(yearurl, mname),
                          'month': u'%s %s (%s)'%(
                                    monthNames[int(mname)-1],yearName,len(posts))}))
                dates.sort()
                dates = [info for m, info in dates]

        dates.reverse()
        return dates

    def isAvailable(self):
        return self.context.dates

    @cache('portlets.blogger.archive', ContextModified)
    def updateAndRender(self):
        return super(BlogArchivePortlet, self).updateAndRender()
