##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
from zojax.blogger.interfaces import IBlogPostPage

from zope import interface
from zope.schema.fieldproperty import FieldProperty

from z3c.form.object import registerFactoryAdapter

from zojax.richtext.field import RichTextProperty


class BlogPostPage(object):
    interface.implements(IBlogPostPage)

    title = None

    text = RichTextProperty(IBlogPostPage['text'])

    position = FieldProperty(IBlogPostPage['position'])



registerFactoryAdapter(IBlogPostPage, BlogPostPage)

# registerFactoryAdapter(IImageRotatorSimpleImage, ImageRotatorSimpleImage)

# registerFactoryAdapter(IImageRotatorButton, ImageRotatorButton)
