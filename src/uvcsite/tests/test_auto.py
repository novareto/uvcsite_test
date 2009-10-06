import z3c.testsetup
import uvcsite

test_suite = z3c.testsetup.register_all_tests('uvcsite',
    layer=uvcsite.tests.FunctionalLayer)
