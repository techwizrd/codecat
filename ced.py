#!/usr/bin/env python

#DO NOT USE THIS FILE FOR DEVELOPMENT. ALL CODE IS BEING REWRITTEN
#AND MIGRATED TO CODECAT.PY

#THIS CODE IS NOT DEPRECATED

import pygtk
pygtk.require('2.0')
import gtk, gtksourceview, mimetypes, os

class Ced:
	def __init__(self):
		self.docnum = 0
		self.documents = []
		
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_size_request(800,600)
		self.window.set_position(gtk.WIN_POS_CENTER)

		self.realbox = gtk.VBox(homogeneous = False, spacing = 0)

		self.initializeMenus()
		self.initializeEditor()
		self.window.add(self.realbox)

		self.openPage(None, "/home/kunal/Projects/ced/ced.py")
		self.openPage(None, None)
		self.openPage(None, None)

		self.openFile(None)

		self.window.show_all()

	def delete_event(self, widget, event, data=None):
		print "delete event occurred"
		return False

	def destroy(self, widget, data=None):
		print "destroy signal occurred"
		gtk.main_quit()

	def initializeMenus(self):
		self.menubar = gtk.MenuBar()
		self.filemenu = gtk.Menu()
		self.filem = gtk.MenuItem("File")
		self.filem.set_submenu(self.filemenu)
		self.menu_new = gtk.MenuItem("New")
		self.menu_new.connect("activate", self.openPage, None)
		self.filemenu.append(self.menu_new)
		self.menu_open = gtk.MenuItem("Open")
		self.menu_open.connect("activate", self.openFile)
		self.filemenu.append(self.menu_open)
		self.menu_exit = gtk.MenuItem("Exit")
		self.menu_exit.connect("activate", self.destroy)
		self.filemenu.append(self.menu_exit)
		self.menubar.append(self.filem)
		self.menubox = gtk.VBox(homogeneous = False, spacing = 0)
		self.menubox.pack_start(self.menubar, False, False, 0)
		self.realbox.pack_start(self.menubox, False, False, 0)
		self.menubox.show()
	
	def initializeEditor(self):
		self.notebook = gtk.Notebook()
		self.pane = gtk.HPaned()
		self.pane.add(self.notebook)
		self.realbox.add(self.pane)

	def openPage(self, widget, filename):
		b = len(self.documents)
		if filename == None:
			self.docnum += 1
			a = [gtksourceview.SourceBuffer(), gtksourceview.SourceLanguagesManager()]
			a.append(a[1].get_language_from_mime_type("text/plain"))
			a[0].set_language(a[2])
			a[0].set_highlight(True)
			a.append(gtksourceview.SourceView(a[0]))
			a[3].set_show_line_numbers(True)
			a.append(gtk.ScrolledWindow())
			a[4].set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			a[4].add(a[3])
			a.append(filename)
			self.window.set_title("Unsaved Document " + str(self.docnum) + " - CodeEDitor")
			self.documents.append(a)
			self.notebook.append_page(self.documents[b][4], gtk.Label(os.path.basename("Unsaved Document" + str(self.docnum))))
			return True
		elif os.path.exists(filename):
			print "opening " + filename
			b = len(self.documents)
			a = [gtksourceview.SourceBuffer(), gtksourceview.SourceLanguagesManager()]
			a.append(a[1].get_language_from_mime_type(mimetypes.guess_type(filename)[0]))
			a[0].set_language(a[2])
			a[0].set_highlight(True)
			a.append(gtksourceview.SourceView(a[0]))
			a[3].set_show_line_numbers(True)
			a[3].set_smart_home_end(True)
			a.append(gtk.ScrolledWindow())
			a[4].set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			a[4].add(a[3])
			a.append(filename)
			d = open(filename)
			a[0].set_text(d.read())
			self.window.set_title(os.path.basename(filename) + " - " + os.path.dirname(filename) + " - CodeEDitor")
			self.documents.append(a)
			self.notebook.append_page(self.documents[b][4], gtk.Label(os.path.basename(filename)))
			return True
		else:
			print filename + " does not exist"
			gtk.MessageDialog(parent=None, flags=gtk.DIALOG_DESTROY_WITH_PARENT, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="File not found").show()
			return False

	def openFile(self, widget, date=None):
		fc = gtk.FileChooserDialog(title='Open File...',
									parent=None,
									action=gtk.FILE_CHOOSER_ACTION_OPEN,
									buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		fc.set_default_response(gtk.RESPONSE_OK)
		response = fc.run()
		if response == gtk.RESPONSE_OK:
			self.openPage(fc, fc.get_filename())
		else:
			print 'not ok'
		fc.destroy()

	def main(self):
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		gtk.main()


print __name__
if __name__ == "__main__":
	CedWin = Ced()
	CedWin.main()
	print "This code be deprecated, yarr! ARR!"
	sys.exit(1)
