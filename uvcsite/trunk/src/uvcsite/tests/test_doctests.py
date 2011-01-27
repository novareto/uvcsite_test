# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 


import doctest
import unittest
import uvcsite.tests

from zope.app.testing.functional import FunctionalDocFileSuite



def test_suite():
    functional = FunctionalDocFileSuite(
        'app.txt', 'api/companyinfo.txt', 'auth/handler.txt',
        'auth/masteruser.txt', 'content/columnoverride.txt',
        'content/container.txt', 'content/folderinit.txt', 'content/content.txt',
        'content/crudviews.txt', 'content/multiple_workflow.txt',
        'content/productfolderutilities.txt', 'content/table.txt',
        'content/views.txt', 'content/withoutclass.txt',
        'extranetmembership/enms.txt', 'homefolder/homefolder.txt',
        'utils/help.txt', 'utils/mail.txt', 'homefolder/views.txt',
        'viewlets/managers.txt', 'viewlets/viewlets.txt',
        'workflow/workflow.txt', 'workflow/basic_workflow.txt',
        'content/ftests/api.py', 'content/ftests/homefoldertest.py', 
        package="uvcsite", 
        optionflags=doctest.ELLIPSIS|
                    doctest.IGNORE_EXCEPTION_DETAIL|
                    doctest.REPORT_NDIFF|
                    doctest.NORMALIZE_WHITESPACE,
        )
    functional.layer = uvcsite.tests.FunctionalLayer
    return functional
