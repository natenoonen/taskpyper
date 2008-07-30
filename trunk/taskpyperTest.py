#!/usr/bin/env python

import unittest;
from taskpyper import *;


#These are semi-standard magic values to track module info
__license__ = u"LGPL"
__version__  = u"0.1.0.16";
__author__ = u"FarMcKon";

_gDebug = False;

#:todo: hide this function from the outside world
def debugprint(*stuffToPrint):
	#Astric indicates that it can handle a list as input
	if (_gDebug):
		print "DEBUG:" + " ".join(stuffToPrint)
		
		
class TaskBlogTest(unittest.TestCase):

	def setUp(self):
		debugprint("setup UnitTests");
		
	def tearDown(self):
		debugprint("setup tearDown");


	def testLoad(self):
		blog = TaskFile("UnitTester.taskpaper")
		self.assert_(blog.tasksRawText)
		self.assert_(blog.sourceFilename)
		self.assert_(blog.fileSynced)

	def testEmpty(self):
		debugprint("testEmpty");

if __name__ == '__main__':
    unittest.main()
