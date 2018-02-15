# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import uvcsite
import doctest
import unittest
import uvcsite.tests

from zope.app.testing.functional import FunctionalDocFileSuite
from zope.app.wsgi.testlayer import BrowserLayer


FunctionalLayer = BrowserLayer(uvcsite, 'ftesting_uvc.zcml')

def test_suite():
    suite = unittest.TestSuite()
    layer = uvcsite.tests.FunctionalLayer
    functional = FunctionalDocFileSuite(
        'app.txt', 'auth/handler.txt',
        'auth/masteruser.txt', 'content/columnoverride.txt',
        'content/container.txt', 'content/folderinit.txt',
        'content/content.txt', 'content/p_reg_integration.txt',
        'content/crudviews.txt', 'content/multiple_workflow.txt',
        'content/productfolderutilities.txt', 'content/table.txt',
        'content/views.txt', 'content/withoutclass.txt',
        'extranetmembership/enms.txt', 'homefolder/homefolder.txt',
        'utils/help.txt', 'utils/mail.txt', 'homefolder/views.txt',
        'viewlets/managers.txt', 'viewlets/viewlets.txt',
        'workflow/workflow.txt', 'workflow/basic_workflow.txt',
        'content/ftests/api.py', 'content/ftests/homefoldertest.py',
        'utils/beaker.txt', 'utils/roles.txt', 'utils/tales.txt',
        'stat/stat.txt', 'auth/group.txt', 'utils/pdf.txt',
        'utils/xml.txt', 'utils/shorties.txt', 'content/productregistration.txt',
        'content/securityviews.txt', 'content/ftests/api_json.py',
        package="uvcsite",
        globs={'__name__': 'uvcsite'},
        optionflags=doctest.ELLIPSIS |
                    doctest.IGNORE_EXCEPTION_DETAIL |
                    doctest.REPORT_NDIFF |
                    doctest.NORMALIZE_WHITESPACE,
    )
    functional.layer = layer
    suite.addTest(functional)
    uvc_layer = uvcsite.tests.UVCBrowserLayer
    test = doctest.DocFileSuite(
        'workflow/workflow_api.txt',
        package='uvcsite',
        globs={'getRootFolder': uvc_layer.getRootFolder},
        optionflags=doctest.ELLIPSIS |
            doctest.IGNORE_EXCEPTION_DETAIL |
            doctest.REPORT_NDIFF |
            doctest.NORMALIZE_WHITESPACE,
    )
    test.layer = uvc_layer
    suite.addTest(test)
    return suite
