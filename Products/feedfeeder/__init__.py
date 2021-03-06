# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger("feedfeeder")
logger.debug('Start initialization of feedfeeder product.')

from zope.i18nmessageid import MessageFactory

from Products.CMFCore import utils as cmfutils
from Products.CMFCore import DirectoryView
from Products.Archetypes.atapi import process_types
from Products.Archetypes import listTypes

from Products.feedfeeder.config import product_globals
from Products.feedfeeder.config import PROJECTNAME
from Products.feedfeeder.config import DEFAULT_ADD_CONTENT_PERMISSION

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/feedfeeder', product_globals)


_ = MessageFactory('feedfeeder')


def initialize(context):
    # imports packages and types for registration
    from Products.feedfeeder import content
    from Products.feedfeeder import interfaces
    from Products.feedfeeder import utilities
    from Products.feedfeeder import contenthandler

    # Make pyflakes happy
    content
    interfaces
    utilities
    contenthandler

    # Initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types=content_types,
        permission=DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors=constructors,
        fti=ftis,
    ).initialize(context)
