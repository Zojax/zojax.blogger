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

from zojax.layoutform import Fields
from zojax.wizard.step import WizardStepForm
from zojax.wizard.interfaces import ISaveable
from zojax.blogger.interfaces import _, IBloggerProduct

from interfaces import IBloggerDestination
from destination import BloggerMailInDestination


class MailInConfigure(WizardStepForm):
    interface.implements(ISaveable)

    fields = Fields(IBloggerDestination)

    title = _('Mail-in')
    label = _('Configure blog mail-in')
    weight = 250

    def getContent(self):
        return IBloggerDestination(getUtility(IBloggerProduct))
