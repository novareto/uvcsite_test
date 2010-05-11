from uvcsite.tests import suiteFromPackage


def test_suite():
    return suiteFromPackage('uvcsite.content.ftests')
