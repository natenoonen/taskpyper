#!/usr/bin/env python

""" dueTasks  a tool for reading a taskpaper file and finding what tasks are
due that day, and printing them to the screen."""

import re
from datetime import datetime
from taskpyper import TaskFile


__version__  = u"0.1.0.9"
gDebug = False;

#:todo: hide this function from the outside world
def debugprint(*stuffToPrint):
	#Astric indicates that it can handle a list as input
	if (gDebug):
		print "DEBUG:" + " ".join(stuffToPrint)


		
def main():
	""" Main statement for running this as a command line tool."""
	from optparse import OptionParser;

	importFilename = "test.taskpaper"
	tpBlob = None
	checkForDue = True
	exportDueType = "stdout"
	targetDatetime = datetime.now()
	
	debugprint('main')
	
	
	#Parse for cmd line values
	optParser = OptionParser()
	optParser.add_option("-i","--inputFilename",dest='filename',help="input file",type='string')
	
	debugprint('parsing')
	(option, arg) = optParser.parse_args();

	if(option.filename and option.filename != ""):
		importFilename = option.filename;
		debugprint('import filename')

	if(importFilename):
		tpBlob =  TaskFile(importFilename)

	if tpBlob and (checkForDue is True):
		dueTasks = tpBlob.findDue(targetDatetime)
		if(exportDueType == "stdout"):
			print "Due Items:"
			for task in dueTasks:
				print str(task)

if __name__ == u"__main__":
	main()
