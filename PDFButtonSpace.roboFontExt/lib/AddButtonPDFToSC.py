from mojo.events import addObserver
from vanilla import *
from mojo.UI import CurrentSpaceCenter, SpaceCenterToPDF
from AppKit import NSUserName

event = "spaceCenterDidOpen" 


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
		file = '/Users/%s/Desktop/RF_space.pdf' % NSUserName()
		SC = CurrentSpaceCenter()
		SpaceCenterToPDF(file, spaceCenter=SC)
		#print "see:", file
		import os
		os.system("open "+file)


AddButtonPDFToSpaceCenter()