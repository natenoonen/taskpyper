#!/usr/bin/env python
import re;
from optparse import OptionParser;
from sys import stdout,stderr;
from datetime import datetime;

from taskpyper import TaskBlob

gDebug = False;

def debugprint(*stuffToPrint):
	#Astric indicates that it can handle a list as input
	if (gDebug is True):
		print "DEBUG:" + str(stuffToPrint)

		
def loadTaskpaperFromFile(filename):
	tpBlob = TaskBlob(filename)
	return tpBlob;

def main():
	""" Main statement for running this as a command line tool """
	importFilename = "/Users/jmck/Documents/test.taskpaper"
	tpBlob = None
	checkForDue = True
	exportDueType = "stdout"
	
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
		tpBlob = loadTaskpaperFromFile(importFilename)

	if tpBlob and (checkForDue is True):
		dueItems = tpBlob.findDue()
		if(exportDueType == "stdout"):
			print "Due Items:"

if __name__ == u"__main__":
	main()
