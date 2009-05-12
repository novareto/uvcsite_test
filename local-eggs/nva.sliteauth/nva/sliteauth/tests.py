import z3c.testsetup
import nva.sliteauth

print "This file is picked up by the testrunner..."

test_suite = z3c.testsetup.register_all_tests('nva.sliteauth')

#suite = test_suite()
#get_basenames_from_suite(suite)
