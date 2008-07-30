#!/usr/bin/env python
"""
Taskpyper is a module of taskaper markup tools written in pthon.
TODO: Document what markup is acceptable here."""

import re;
from optparse import OptionParser;
from sys import stdout,stderr
from datetime import datetime

#These are semi-standard magic values to track module info
__license__ = u"LGPL"
__version__  = u"0.1.0.16";
__author__ = u"FarMcKon";

#Global values 
_gDebug = True;


def debugprint(*stuffToPrint):
	""" Debugging tool """
	#Astric indicates that it can handle a list as input
	if (_gDebug):
		print "DEBUG:" + " ".join(stuffToPrint)


class TaskFile():
	""" TaskFile class is used to managed a group of tasks	stored in a file. It contains 
	accessory functions to make managing that file eaiser	"""

	tasksRawText = None;   #the raw text from the file
	sourceFilename = None; #the source/destination file
	fileSynced = None; 	   #flag if the rawText and sourceFile are in sync


	def __init__(self,filename=None):
		""" Create the TaskFile object from a file"""
		self.load(filename)
		

	def load(self,filename):
		""" Load a text file of tasks into this TaskFile object """
		debugprint( 'creating task blob from %s' %filename)
		
		if filename is not None:
			debugprint('Loading from file %(file)s' % {'file': filename})
			fh = open(filename,'r')
			if(fh):
				self.tasksRawText = fh.read()	
				self.sourceFilename = filename
				self.fileSynced = True;
				fh.close()
				del fh;
				stdout.write('file loaded OK');
		else: #filename in not None
			self.tasksRawText = None;
			self.fileSynced = None;
			stdout.write('no load file specified');
						

	def autobackup(self, backupFilename=None):
		""" backup the objects rawText data to the given filename.  If no name is given, backup 
		to an name autogenerated by the time the funciton is called. This does NOT set the sync
		bit."""
		if backupFilename is None:
			now = datetime.now()
			nowTxt = now.strftime("%Y.%m.%d.%H.%M.%S")
			backFilename = self.sourceFilename + "." + nowTxt +".backup"
			debugprint("autobackup filename" + backFilename)
			fh = open(backFilename,"w+")
			fh.write(self.tasksRawText)
			fh.close();
			del fh;

	def removeExactMatch(self,exactTaskText):
		"""IF the passed text EXACTLY matches a task,that task is removed from the internal 
		rawText stream. fileSynced is set to false if any modification took place"""
		if exactTaskText:
			#if exactTaskText[-1] != '\n':
			#	exactTaskText = exactTaskText
			regger = re.compile(re.escape(exactTaskText));
			#print 'exact task text: '+ exactTaskText
			#print regger
			match = regger.search(self.tasksRawText,re.M);
			#print 'match: ' + str(match)
			if (match):
				print 'match found'
				re.sub('',self.tasksRawText)
				self.fileSynced = False;
			else:
				print 'no match found'
			
		else:
			print "no text FAIL!"
		#make sure we have an exact whole line match
		#and nuke it from the lastRawRead
		#tpBlob.removeExactMatch(taskMatches[0])


	def findTaskByMatching(self,taskTextToFind):
		"""Takes a string, tries to find all tasks that have that text in it, andthen returns an
		array of all tasks that matched the line"""
		debugprint( 'find task by text: %s' % taskTextToFind)
		matchedLines = []
		matchReg = re.compile(re.escape(taskTextToFind), re.I)
		for x in self.tasksRawText.split('\n'):
			if (matchReg.search(x) != None):
				matchedLines.append(x)
				
		return matchedLines

		

	def findDue(self, targetDT,skipDoneTasks=True, lang="EN"):
		""" This function scans for items due that match the @date with the ISO format date info 
		matching the passed datetime (targetDT). If the targetDT is the same day as the current 
		system information, @today, @tonight and other patterns are added to thet search."""
		duePatterns = ["\s@due\s","\s@todo"]		
		dueItems = []
		#ISO pattern xxx.xx.xx or xxxx-xx-xx
		todayDue = u"\s@due\(%(year)04d(-|.| )%(month)02d(-|.| )%(day)02d\)" %  \
					{'year':targetDT.year, 'month':targetDT.month, 'day':targetDT.day}
		duePatterns.append(todayDue)
			
		#if today is targetDT, add some extra patterns	
		now = datetime.now()
		if(targetDT.year == now.year and targetDT.month == now.month and targetDT.day == now.day):
			duePatterns.extend([u"\s@today",u"\s@tonight"])

		#local language pattern if we ahve it
		duePatterns.append(u"\s@" +now.strftime("%A")+u"\S") #full day name
		duePatterns.append(u"\s@" +now.strftime("%a")+u"\S") #abbr day name
		
		#if(isoWeekdaySets.has_key(lang)):
		#	weekdays = isoWeekdaySets[lang]
		#	if weekdays.has_key(now.isoweekday()) :
		#		str = u"\s@" + weekdays[now.isoweekday()];
		#		debugprint(str)
		#		duePatterns.append(str)
		#		*/

		#:TODO: if tomorrow is targetDT, add some extra patterns
			
		#:TODO: if yesterday was targetDT, add some extra patterns


		#serch for the matches
		for task in self.tasksRawText.split('\n'):
			negatorPattern = u"\s@done"
			negatorReg = re.compile(negatorPattern)
			#TODO add ability to grab 'sub-issues'
			for pattern in duePatterns:
				#print '  doing pattern %s' % pattern
				dueReg = re.compile(pattern, re.I);
				if(dueReg.search(task)):
					if((skipDoneTasks == False) or (negatorReg.search(task) == None) ):
						dueItems.append(task);
						#prevIssueIndentLvl = X;
						debugprint('due item found: %s' % task)
						
		#TODO: strip duplicats from dueItems
		
		return dueItems;

	def findPastDue(self):
		#import datetime;
		#today = datetime.date.today()
		dueWithDate = [];
		for x in self.tasksRawText.split('\n'):
			pastDueReg = re.compile(u"\s@due\([0-9]{4}-[0-9]{2}-[0-9]{2}\)");
			if(pastDueReg.search(x)):
				dueWithDate.append(x)
				#print 'due found %s' % x

	def setIsoDates( baseDateTime = datetime.now()):
		"""This funciton scans the file for  all dates with @somedayname and 
		converts them to @event(IsoDate) or @due (IsoDate)
		"""
		
		debugprint("Boo")
		
	
#	def updateAutomatics(self):
#		print "Testing UpdateAutomatics"
#		x = self.findAutomatics()

#	def findAutomatics(self):
#		"""returns a list of automated items from the raw text"""
#		matchAutomatedTag = []
#		for x in self.tasksRawText.split('n'):
#			print 'bar'
#			autoReg = re.compile(ur"@auto",re.I);
#			z = autoReg.search(x)
#			print z
#			if(z):
#				print 'baz'
#				print 'automated item found %s' % x
#				for c in range(0,len(z.groups())) :
				
#					print "Groups %d: %s " % c, z.groups(c) 
#				matchAutomatedTag.append(x)
#		return matchAutomatedTag

