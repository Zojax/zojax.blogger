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
from zope import interface
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIds
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zojax.content.space.interfaces import ISpace
from zojax.content.draft.interfaces import IDraftContent

from interfaces import IBlog


class CategoriesVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        while True:
            if IBlog.providedBy(context):
                break

            if IDraftContent.providedBy(context):
                context = context.getLocation()
                if ISpace.providedBy(context):
                    context = context.get('blog')
                break

            context = getattr(context, '__parent__', None)
            if context is None:
                break

        if context is None:
            return SimpleVocabulary(())

        ids = getUtility(IIntIds)

        categories = []
        for category in context['category'].values():
            try:
                id = ids.getId(removeAllProxies(category))
            except:
                continue

            term = SimpleTerm(id, str(id), category.title)
            term.description = category.description

            categories.append((category.title, term))

        categories.sort()
        return SimpleVocabulary([term for title, term in categories])
