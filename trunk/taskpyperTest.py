import unittest;
import taskpyper;


__version__  = u"0.1.0.10"
gDebug = True;

#:todo: hide this function from the outside world
def debugprint(*stuffToPrint):
	#Astric indicates that it can handle a list as input
	if (gDebug):
		print "DEBUG:" + " ".join(stuffToPrint)
		
		
class TaskBlogTest(unittest.TestCase):

	blob = None
#	def __init__():
#		debugprint("Initalizing UnitTests");
	
	def setUp(self):
		blog = new TaskBlob("UnitTester.taskpaper")
		debugprint("setup UnitTests");
		
	def tearDown(self):
		debugprint("setup tearDown");


	def testLoad(self):
		blog = new TaskBlob("UnitTester.taskpaper")
		self.assert
		debugprint("setup UnitTests");

	def testEmpty(self):
		debugprint("testEmpty");

if __name__ == '__main__':
    unittest.main()
