# coding=utf-8
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
from AppKit import *
from defconAppKit.windows.baseWindow import BaseWindowController
import subprocess


event = "spaceCenterDidOpen" 

PDFKey = "nl.thomjanssen.PDF"
_PDFFileNameKey = "%s.FileName" % PDFKey
_PDFFolderPathKey = "%s.FolderPath" % PDFKey
_PDFFolderKey = "%s.Folder" % PDFKey
_PDFTimeStampOnOffKey = "%s.TimeStampOnOff" % PDFKey
_PDFTimeStampKey = "%s.TimeStamp" % PDFKey
_PDFOpenPDFKey = "%s.OpenKey" % PDFKey
_PDFTextLimitKey = "%s.TextLimit" % PDFKey

popUpItems = [
	"PDF",
	"Blur",
	"Tracking",
	"Random",
	"Selection",
	]

class Tracker(BaseWindowController):
	def __init__(self):
		self.trackingValue = 0
		self.w = FloatingWindow((250, 45), "Tracking %s" % str(self.trackingValue))
		self.w.s = Slider((10, 10, -30, 22), 
			minValue=-100,
			maxValue=100,
			value=50,
			callback=self.tracker, 
			continuous=True)
		self.w.c = CheckBox((-25, 10, -10, 22),"",callback=self.tracker)
		self.w.c.set(True)
		self.setUpBaseWindowBehavior()
		self.w.open()
		self.tracker(None)
	def tracker(self,sender):
		if self.w.c.get():
			value = self.w.s.get()
		else:
			value = 0
		self.doTracking(value)
	def doTracking(self, value):
			sp = CurrentSpaceCenter()
			# if there is no space center
			if sp is None:
				# do nothing
				return
			sp.setTracking(value)
			self.w.setTitle("Tracking %s" % str(int(value)))
	def windowCloseCallback(self, sender):
		self.doTracking(0)


class Blurryfyer(BaseWindowController):
	def __init__(self):
		# create a window
		self.w = FloatingWindow((250, 45), "Blurryfyer")
		# create a slider
		self.w.s = Slider((10, 10, -30, 22), 
		minValue=0,
		maxValue=100,
		value=50,
		callback=self.blurryfyerCallback, 
		continuous=False)
		self.w.c = CheckBox((-25, 10, -10, 22),"",callback=self.blurryfyerCallback)
		self.w.c.set(True)
		# open the window
		self.setUpBaseWindowBehavior()
		self.w.open()
		self.blurryfyerCallback(None)
	def blurryfyerCallback(self,sender):
		if self.w.c.get():
			# get the value from the slider
			value = self.w.s.get()
			# get the current space center		
		else:
			value = 0
		self.blur(value)
	def blur(self, value):
			sp = CurrentSpaceCenter()
			# if there is no space center
			if sp is None:
				# do nothing
				return
			# get the line view (this is embedded into a scroll view)
			view = sp.glyphLineView.contentView()
			# create the filter
			blur = CIFilter.filterWithName_("CIGaussianBlur")
			# set the filter defaults
			blur.setDefaults()
			# change the input radius for the blur
			blur.setValue_forKey_(value, "inputRadius")
			# collect all filters in a list
			filters = [blur]
			# tel the view to use layers
			view.setWantsLayer_(True)
			# set the filters into the view
			view.setContentFilters_(filters)
	def windowCloseCallback(self, sender):
		self.blur(0)


class FunWithTheSpaceCenter(object):
		
	def __init__(self):
		
		addObserver(self, "addButton", event)
	
	def addButton(self, sender):

		buttonWidth = 60

		sp = CurrentSpaceCenter()
 
		l, t, w, h = sp.top.glyphLinePreInput.getPosSize()
		sp.top.glyphLinePreInput.setPosSize((l + buttonWidth+10, t, w, h))
 
		l, t, w, h = sp.top.glyphLineInput.getPosSize()
		sp.top.glyphLineInput.setPosSize((l + buttonWidth+10, t, w, h))
 
		sp.PopUp = PopUpButton((10, 10, buttonWidth, 22), popUpItems, callback=self.buttonHitCallback)
				
	def buttonHitCallback(self, sender):
		if popUpItems[sender.get()] == "PDF":
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

			filename = filename.replace("%ufo", os.path.splitext(os.path.basename(CurrentFont().path))[0])
			
			SC = CurrentSpaceCenter()
			filename = filename.replace("%text", SC.getRaw()[0:int(getExtensionDefault(_PDFTextLimitKey))])

			
			SpaceCenterToPDF(filename, spaceCenter=SC)

			if getExtensionDefault(_PDFOpenPDFKey):
				try:
					os.system("open '%s'" % filename)
				except:
					subprocess.call(["open", "-R", filename])

		if popUpItems[sender.get()] == "Blur":
			Blurryfyer()
		if popUpItems[sender.get()] == "Tracking":
			Tracker()
		if popUpItems[sender.get()] == "Random":
			from random import shuffle

			SC = CurrentSpaceCenter()
			txt = CurrentSpaceCenter().get()
			shuffle(txt)
			l = []
			for i in range(len(txt)):
				l.append(txt.pop())
			SC.set(l)
		if popUpItems[sender.get()] == "Selection":
			txt = []
			f = CurrentFont()
			for gn in f.glyphOrder:
				if f[gn].selected:
					txt.append("/%s" % gn)
			SC = CurrentSpaceCenter()
			SC.set(txt)

FunWithTheSpaceCenter()