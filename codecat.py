#!/usr/bin/env python
#
# Copyright (C) 2009 techwizrd <theninja@Bluedevs.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import sys

APP_NAME	= 'codecat'
APP_VERSION	= '0.1'
__author__	= 'techwizrd'
__email__	= 'theninja@Bluedevs.net'
__version__	= '0.1'

if sys.platform == 'linux2':
	# Set process name.  Only works on Linux >= 2.1.57.
	try:
		import dl
		libc = dl.open('/lib/libc.so.6')
		libc.call('prctl', 15, 'codecat\0', 0, 0, 0) # 15 is PR_SET_NAME
	except:
		pass

try:
	import pygtk
	pygtk.require('2.0')
except ImportError:
	print "PyGTK 2.0 not found!"
	raise SystemExit
try:
	import gobject
	gobject.threads_init()
except Exception, e:
	print str(e)
	raise SystemExit
try:
	import gtk
	import gtksourceview
	import mimetypes
	import os
	#import gettext
except ImportError, e:
	print "%s found!" % e
	raise SystemExit
except Exception, e:
	print str(e)
	raise SystemExit

class CodeCatWin:
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_size_request(800,600)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_title("CodeCat")
		
		self.initializeMenus()
		self.initializeNotebook()
		
		self.bigbox = gtk.VBox(False, 0)
		self.window.add(self.bigbox)
		self.bigbox.pack_start(self.menubar, False, False, 0)
		#self.bigbox.pack_start(self.menubar, False)
		self.hpane = gtk.HPaned()
		#self.bigbox.pack_start(self.hpane, False, False, 0)
		self.bigbox.add(self.hpane)
		self.hpane.add(self.notebook)
		
		self.window.show_all()
		self.main()

	def initializeMenus(self):
		self.uimanager = gtk.UIManager()
		try:
			self.uimanager.add_ui_from_file("./menus.xml")
			self.actiongroup = gtk.ActionGroup('CodeCat')
			self.actiongroup.add_actions([('Quick Open', gtk.STOCK_OPEN,
											'Quick _Open', None, "Quickly Open a File",
											self.quickOpen),
										('Quit', gtk.STOCK_QUIT, '_Quit',
											None, 'Quit CodeCat', gtk.main_quit),
										('File', None, '_File')])
			self.uimanager.insert_action_group(self.actiongroup, 0)
			self.accelgroup = self.uimanager.get_accel_group()
			self.window.add_accel_group(self.accelgroup)
		except Exception, e:
			print str(e)
			sys.exit(1)
		self.menubar = self.uimanager.get_widget("/MenuBar")

	def initializeToolbar(self):
		pass

	def initializeNotebook(self):
		self.notebook = gtk.Notebook()
		a = CodeCatEditor(filename="/home/kunal/Projects/ced/codecat.py")
		b = CodeCatEditor(filename="/home/kunal/Projects/ced/ced.py")
		c = CodeCatEditor(filename="/home/kunal/Projects/ced/menus.xml")
		d = CodeCatEditor(filename="/home/kunal/Desktop/kparse.php")
		c.splitHoriz(None, d)
		b.splitVert(None, c)
		a.splitHoriz(None, b)
		#c.close()
		self.notebook.set_tab_reorderable(a.hpane, True)
		self.notebook.append_page(a.hpane, gtk.Label("Scratch Workspace 2"))
		self.pages = []
		for x in range(0,5):
			self.pages.append(gtk.Label("lolz"))
			self.notebook.append_page(self.pages[x], gtk.Label("Workspace %s" % (x + 1)))
			self.notebook.set_tab_reorderable(self.pages[x], True)
		#a = gtk.HPaned()
		#d = gtk.Frame()
		#d.add(gtksourceview.SourceView(gtksourceview.SourceBuffer()))
		#a.add(d)
		#b = gtk.VPaned()
		#a.add(b)
		#b.add(gtksourceview.SourceView(gtksourceview.SourceBuffer()))
		#b.add(gtksourceview.SourceView(gtksourceview.SourceBuffer()))
		#self.workspaces = [[]]
		#self.notebook.append_page(a, gtk.Label("Scratch Workspace")

	def initializeSidebar(self):
		pass
	
	def quickOpen(self):
		pass

#	def delete_event(self, widget, event, data=None):
#		#print "delete event occurred"
#		return False

#	def destroy(self, widget, data=None):
#		print "Exiting CodeCat"
#		gtk.main_quit()

	def main(self):
		self.window.connect("delete_event", gtk.main_quit)
		self.window.connect("destroy", gtk.main_quit)

class CodeCatEditor(gtk.HPaned):
	def __init__(self, filename=None):
		self.hpane = gtk.HPaned()
		self.vpane = gtk.VPaned()
		self.hpane.add(self.vpane)
		self.scrollwin = gtk.ScrolledWindow()
		self.scrollwin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.theframe = gtk.Frame()
		self.theframe.set_label(filename)
		#self.theframe.add(self.scrollwin)
		self.vpane.add(self.theframe)
		self.eventbox = gtk.EventBox()
		self.theframe.add(self.eventbox)
		self.eventbox.add(self.scrollwin)
		self.sourcebuffer = gtksourceview.SourceBuffer()
		self.sourceview = gtksourceview.SourceView(self.sourcebuffer)
		self.filename = filename
		if self.filename != None:
			self.loadFile(None, self.filename)
		self.sourcebuffer.set_highlight(True)
		self.sourceview.set_show_line_numbers(True)
		self.sourceview.set_smart_home_end(True)
		self.scrollwin.add(self.sourceview)
		self.sourceview.connect("button_press_event", self.contextMenu, None)
		self.hpane.show_all()
	
	def splitHoriz(self, widget, newEd=None):
		if newEd == None:
			newEd = CodeCatEditor()
		self.vpane.add(newEd.hpane)
	
	def splitVert(self, widget, newEd=None):
		if newEd == None:
			newEd = CodeCatEditor()
		self.hpane.add(newEd.hpane)
	
	def loadFile(self, widget, filename):
		try:
			codefile = open(filename, 'r')
			a = gtksourceview.SourceLanguagesManager().get_language_from_mime_type(mimetypes.guess_type(filename)[0])
			self.sourcebuffer.set_language(a)
			self.sourcebuffer.set_text(codefile.read())
			codefile.close()
		except Exception, e:
			print str(e)
	
	def saveFile(self, widget, filename):
		try:
			codefile = open(filename, 'w')
			codefile.write(self.sourcebuffer.get_text())
			codefile.close()
		except Exception, e:
			print str(e)
	
	def close(self, widget):
		self.hpane.destroy()
	
	def contextMenu(self, widget, event, data=None):
		print "conte"
		if(event.button != 3):
			return False 
		self.cMenu = gtk.Menu()
		self.cMenuItems = [gtk.MenuItem("Save File"), gtk.MenuItem("Split Horizontally"),
							gtk.MenuItem("Split Vertically"), gtk.MenuItem("New Workspace"),
							gtk.MenuItem("Close Document")]
		self.cMenuItems[1].connect("activate", self.splitHoriz)
		self.cMenuItems[2].connect("activate", self.splitVert)
		self.cMenuItems[4].connect("activate", self.close)
		for x in self.cMenuItems:
			x.show()
			self.cMenu.append(x)
		self.cMenu.popup(None, None, None, event.button, event.time, None) 
		return False

if __name__ == "__main__":
	print "CodeCat v%s" % __version__
	codecat = CodeCatWin()
	gtk.main()
	print codecat.notebook.get_current_page()
