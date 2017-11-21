from vanilla import *
from vanilla.dialogs import getFolder
from mojo.extensions import getExtensionDefault, setExtensionDefault, registerExtensionDefaults
from lib.UI.statusBar import StatusBar
from os import getlogin
from defconAppKit.windows.baseWindow import BaseWindowController
from lib.scripting import extensionTools
from AppKit import *

PDFKey = "nl.thomjanssen.PDF"
_PDFFileNameKey = "%s.FileName" % PDFKey
_PDFFolderPathKey = "%s.FolderPath" % PDFKey
_PDFFolderKey = "%s.Folder" % PDFKey
_PDFTimeStampOnOffKey = "%s.TimeStampOnOff" % PDFKey
_PDFTimeStampKey = "%s.TimeStamp" % PDFKey
_PDFOpenPDFKey = "%s.OpenKey" % PDFKey
_PDFTextLimitKey = "%s.TextLimit" %PDFKey


defaults = dict()
defaults[_PDFFileNameKey] = 'RoboFontSpaceCenter'
defaults[_PDFFolderPathKey] = '/Users/%s/Desktop' % getlogin()
defaults[_PDFFolderKey] = 0
defaults[_PDFTimeStampOnOffKey] = False
defaults[_PDFTimeStampKey] = "%y%m%d_%H%M%S"
defaults[_PDFOpenPDFKey] = True
defaults[_PDFTextLimitKey] = 5
registerExtensionDefaults(defaults)

extra = """Extra options for file name:
%ufo = ufo file name
%text = actual text in the spacecenter"""

class PDFSettings(object):
	def __init__(self):
		width = 300
		height = 400
		y=7
		self.w = FloatingWindow((width, height), "PDF Settings")

		# file name
		self.w.fileNameText = TextBox((10,y,-10,22), "File name", sizeStyle='small')
		self.w.fileNameEdit = EditText((10,y+22,-10,25), text=getExtensionDefault(_PDFFileNameKey), callback=self._warning, continuous=False)
		
		y+=60
		self.w.txt = TextBox((10,y,-10,100), extra, sizeStyle='small')
		self.w.line0 = HorizontalLine((10,y+55,-10,1))
		
		y+=70
		# time stamp
		self.w.timeStampOnOff = CheckBox((10, y, -10, 25), "Add timestamp:", value=getExtensionDefault(_PDFTimeStampOnOffKey), callback=self._warning, sizeStyle='small')
		self.w.timeStamp = EditText((125,y, -10, 25), text=getExtensionDefault(_PDFTimeStampKey), continuous=False, callback=self._warning)
		self.w.timestampInfo = Button((125,y+28,-10,20),"timestamp syntax docs", callback=self.timeStampInfoCallback, sizeStyle='small')

		self.w.line1 = HorizontalLine((10,y+60,-10,1))
		
		y+=70
		self.w.limitText = TextBox((10,y+5, -10,25), "Limit %text characters:", sizeStyle='small')
		self.w.limitEdit = EditText((170,y,-10,25), "5", placeholder="int")
		self.w.lineLimit = HorizontalLine((10,y+35,-10,1))

		y+=50
		# folder
		self.w.folderText = TextBox((10,y,-10,25), "Folder", sizeStyle='small')
		self.w.folder = RadioGroup((10,y+10,-100,35), ["UFO folder","Other"], callback=self._warning, sizeStyle='small', isVertical = False)
		self.w.folder.set(getExtensionDefault(_PDFFolderKey))
		self.w.folderPath = EditText((10,y+40,-10,25), getExtensionDefault(_PDFFolderPathKey), readOnly=True)
		self.w.folderChange = Button((-100,y+14,-10,25), "Change folder", callback=self.changeFolderPath, sizeStyle='small')

		self.w.line2 = HorizontalLine((10,y+80,-10,1))

		
		y += 90
		# open PDF
		self.w.openPDF = CheckBox((10, y, -10, 25), "Open PDF immediately", value=getExtensionDefault(_PDFOpenPDFKey), callback=self._warning, sizeStyle='small')
		
		# status
		self.w.statusBar = StatusBar((0, -20, 0, 0))

		self.w.bind("close",self._close)
		self.w.open()
	
	def _warning(self, sender):
		if sender == self.w.timeStampOnOff:
			if sender.get():
				self.w.timeStamp.enable(1)
			else: 
				self.w.timeStamp.enable(0)
				
		if sender == self.w.folder:
			if sender.get():
				self.w.folderPath.enable(1)
			else: 
				self.w.folderPath.enable(0)
				
		self.w.statusBar.set(['close this window to save'],  fadeOut=True, warning=True)
		
	def _close(self, sender):
		setExtensionDefault(_PDFFileNameKey, self.w.fileNameEdit.get())
		setExtensionDefault(_PDFTimeStampOnOffKey, self.w.timeStampOnOff.get())
		setExtensionDefault(_PDFTimeStampKey, self.w.timeStamp.get())

		setExtensionDefault(_PDFTextLimitKey, int(self.w.limitEdit.get()))

		setExtensionDefault(_PDFFolderKey, self.w.folder.get())
		setExtensionDefault(_PDFFolderPathKey, self.w.folderPath.get())

		setExtensionDefault(_PDFOpenPDFKey, self.w.openPDF.get())

	def changeFolderPath(self,sender):
		newPath = getFolder()
		self.w.folderPath.set(newPath[0])
		setExtensionDefault(_PDFFolderPathKey, newPath[0])

	def timeStampInfoCallback(self, sender):
		self.b = Window((800, 450), minSize=(200, 200), title='Timestamp Docs')
		items = [
			dict(image=NSImage.imageNamed_(NSImageNameGoLeftTemplate), toolTip='back'), 
			dict(image=NSImage.imageNamed_(NSImageNameGoRightTemplate), toolTip='forward')
		]
		toolbarBackForward = extensionTools.ToolbarWeb((100, 25), items, 'one')
		self.visitButton = extensionTools.ToolBarButton((100, 25))
		toolbarItems = [
			dict(itemIdentifier='navigation', label='', view=toolbarBackForward, callback=self.backAndForwardCallback), 
		]
		self.b.addToolbar(toolbarIdentifier='helpViewToolbar', toolbarItems=toolbarItems, addStandardItems=False)
		toolbar = self.b.getNSWindow().toolbar()
		toolbar.setDisplayMode_(NSToolbarDisplayModeIconOnly)
		self.b.w = extensionTools.HTMLView((0, 0, 0, 0))
		self.b.w.setFrameDelegate(toolbarBackForward)
		self.b.w.setHTMLPath("https://docs.python.org/2/library/time.html#time.strftime")
		self.b.open()

	def backAndForwardCallback(self, sender):
		if sender.selectedSegment():
			self.b.w.goForward()
		else:
			self.b.w.goBack()
PDFSettings()
