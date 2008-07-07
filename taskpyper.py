#!/usr/bin/env python

""" taskpyper is a module of taskaper markup tools written in pthon."""

import re;
from optparse import OptionParser;
from sys import stdout,stderr;
from datetime import datetime;

__name__ = "taskpyper"
__version__ "0.1.0.4"

gDebug = False;

def debugprint(*stuffToPrint):
	#Astric indicates that it can handle a list as input
	if (gDebug):
		print "DEBUG:" + str(stuffToPrint)

class TaskBlob():
	""" TaskBlob is a class that contains a text file of tasks
	and accessory functions.
	TODO:
	"""
	lastReadRawTxt = None;
	sourceFilename = None;

	def __init__(self,filename=None):
		self.load(filename)

	def load(self,filename):
		debugprint( 'creating task blob from %s' %filename)
		if filename is not None:
			debugprint('Loading from file %(file)s' % {'file': filename})
			fh = open(filename,'r')
			if(fh):
				self.lastReadRawTxt = fh.read()	
				fh.close()
				self.sourceFilename = filename
				print 'load file OK'	
		else: #if filename is None
			print 'No file to load'
			self.lastReadRawTxt = None;
		
		if self.lastReadRawTxt is not None :
			#parse/built it out
			debugprint( 'reading tasks from list')
			taskReg = re.compile(u"\s*- .*\n")
			taskIter = taskReg.finditer(self.lastReadRawTxt)
				
	def autoBackup(self):
		print 'starting backup'
		print 'source filename: '
		print self.sourceFilename
		timeNow = datetime.now();
		newFilenameArray = [self.sourceFilename,];
		newFilenameArray.append(str(timeNow.year))
		newFilenameArray.append(str(timeNow.month))
		newFilenameArray.append(str(timeNow.day))
		newFilenameArray.append(str(timeNow.hour))
		newFilenameArray.append(str(timeNow.min))
		newFilenameArray.append(str("BACKUP"))
		backupFilename = ".".join(newFilenameArray)
		print 'backup filename'
		print str(backupFilename)
		
		

	def findDue(self):
		#print 'running findDue'
		for x in self.lastReadRawTxt.split('\n'):
			#look for the following keys:
			#@due #@today #today @date(THIS_DAY)
			#print 'x is %s' %x
			duePatterns = [u"\s@today",u"\s@tonight"]
			today = datetime.now();
			todayDue = u"\s@due\(%(year)04d(-|.| )%(month)02d(-|.| )%(day)02d\)" %  \
							{'year':today.year, 'month':today.month, 'day':today.day}
			#debugprint(todayDue)
			duePatterns.append(todayDue)
			#ISO pattern xxx.xx.xx or xxxx-xx-xx
			negatorPattern = u"\s@done"
			negatorReg = re.compile(negatorPattern)
			for pattern in duePatterns:
				#print '  doing pattern %s' % pattern
				dueReg = re.compile(pattern);	
				if(dueReg.search(x)): # and negatorReg.search(x) == None):
					print 'due item found: %s' % x


	def updateAutomatics(self):
		print "Testing UpdateAutomatics"
		x = self.findAutomatics()

	def findAutomatics(self):
		"""returns a list of automated items from the raw text"""
		matchAutomatedTag = []
		for x in self.lastReadRawTxt.split('n'):
			print 'bar'
			autoReg = re.compile(ur"@auto",re.I);
			z = autoReg.search(x)
			print z
			if(z):
				print 'baz'
				print 'automated item found %s' % x
				for c in range(0,len(z.groups())) :
				
					print "Groups %d: %s " % c, z.groups(c) 
				matchAutomatedTag.append(x)
		return matchAutomatedTag

	def findPastDue(self):
		#import datetime;
		#today = datetime.date.today()
		dueWithDate = [];
		for x in self.lastReadRawTxt.split('\n'):
			pastDueReg = re.compile(u"\s@due\([0-9]{4}-[0-9]{2}-[0-9]{2}\)");
			if(pastDueReg.search(x)):
				dueWithDate.append(x)
				#print 'due found %s' % x	
