#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, gtksourceview

class Ced:
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		#self.sourcebuffers = []
		self.vbox = gtk.VBox(homogeneous = False, spacing = 0)
		self.window.resize(400,400)
		self.window.add(self.vbox)
		self.newEditor()
		self.window.show_all()

	def delete_event(widget, event, data=None):
		print "delete event occurred"
		return False

	def destroy(widget, data=None):
		print "destroy signal occurred"
		gtk.main_quit()
	
	def newEditor(self):
		self.sourcebuffer = gtksourceview.SourceBuffer()
		self.langmanager = gtksourceview.SourceLanguagesManager()
		self.codelang = self.langmanager.get_language_from_mime_type("text/x-python")
		self.sourcebuffer.set_language(self.codelang)
		self.sourcebuffer.set_highlight(True)
		self.view = gtksourceview.SourceView(self.sourcebuffer)
		self.view.set_show_line_numbers(True)
		self.scrolledwindow = gtk.ScrolledWindow()
		self.scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.scrolledwindow.add(self.view)
		self.vbox.add(self.scrolledwindow)

	def main(self):
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		gtk.main()


print __name__
if __name__ == "__main__":
	CedWin = Ced()
	CedWin.main()
