"""
TODO:
	file name fontname / stylename prefixes
	timestamp different prefixes?
	bug: files in dropbox do not open!?
"""


from mojo.events import addObserver
from vanilla import *
from mojo.UI import CurrentSpaceCenter, SpaceCenterToPDF
from mojo.extensions import getExtensionDefault
import os

event = "spaceCenterDidOpen" 

PDFKey = "nl.thomjanssen.PDF"
_PDFFileNameKey = "%s.FileName" % PDFKey
_PDFFolderPathKey = "%s.FolderPath" % PDFKey
_PDFFolderKey = "%s.Folder" % PDFKey
_PDFTimeStampOnOffKey = "%s.TimeStampOnOff" % PDFKey
_PDFTimeStampKey = "%s.TimeStamp" % PDFKey
_PDFOpenPDFKey = "%s.OpenKey" % PDFKey


class AddButtonPDFToSpaceCenter(object):
		
	def __init__(self):
		
		addObserver(self, "addButton", event)
	
	def addButton(self, sender):

		sp = CurrentSpaceCenter()
 
		l, t, w, h = sp.top.glyphLinePreInput.getPosSize()
		sp.top.glyphLinePreInput.setPosSize((l + 50, t, w, h))
 
		l, t, w, h = sp.top.glyphLineInput.getPosSize()
		sp.top.glyphLineInput.setPosSize((l + 50, t, w, h))
 
		sp.PDFButton = Button((10, 10, 40, 22), "PDF", callback=self.buttonHitCallback)
				
	def buttonHitCallback(self, sender):
		if getExtensionDefault(_PDFFolderKey) == 0:
			folder = os.path.dirname(os.path.realpath(CurrentFont().path))
		else: 
			folder = getExtensionDefault(_PDFFolderPathKey)
		
		if getExtensionDefault(_PDFTimeStampOnOffKey):
			from time import strftime
			timestamp = "_%s" % strftime('%s' % getExtensionDefault(_PDFTimeStampKey))
		else:
			timestamp = ""

		filename = '%s/%s%s.pdf' % (folder,getExtensionDefault(_PDFFileNameKey),timestamp)

		SC = CurrentSpaceCenter()
		SpaceCenterToPDF(filename, spaceCenter=SC)

		if getExtensionDefault(_PDFOpenPDFKey):
			os.system("open "+filename)


AddButtonPDFToSpaceCenter()