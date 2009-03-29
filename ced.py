#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, gtksourceview, mimetypes, os

class Ced:
	def __init__(self):
		self.docnum = 0
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.pane = gtk.HPaned()
		self.documents = []
		self.vbox = gtk.VBox(homogeneous = False, spacing = 0)
		self.notebook = gtk.Notebook()
		self.vbox.add(self.notebook)
		self.window.resize(800,600)
		self.window.add(self.pane)
		self.pane.add(self.vbox)
		self.window.show_all()

	def delete_event(widget, event, data=None):
		print "delete event occurred"
		return False

	def destroy(widget, data=None):
		print "destroy signal occurred"
		gtk.main_quit()
	
	def initializeMenus():
		pass

	def newEditor(self, filename):
		self.documents.append([gtksourceview.SourceBuffer(), gtksourceview.SourceLanguagesManager()])
		a = len(self.documents)-1
		self.documents[a].append(self.documents[a][1].get_language_from_mime_type(mimetypes.guess_type(filename)[0]))
		self.documents[a][0].set_language(self.documents[a][2])
		self.documents[a][0].set_highlight(True)
		self.documents[a].append(gtksourceview.SourceView(self.documents[a][0]))
		self.documents[a][3].set_show_line_numbers(True)
		self.scrolledwindow = gtk.ScrolledWindow()
		self.scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.scrolledwindow.add(self.documents[a][3])
		self.notebook.append_page(self.scrolledwindow, None)

	def openPage(self, filename):
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
		elif os.path.exists(filename):
			print "opening " + filename
			b = len(self.documents)
			a = [gtksourceview.SourceBuffer(), gtksourceview.SourceLanguagesManager()]
			a.append(a[1].get_language_from_mime_type(mimetypes.guess_type(filename)[0]))
			a[0].set_language(a[2])
			a[0].set_highlight(True)
			a.append(gtksourceview.SourceView(a[0]))
			a[3].set_show_line_numbers(True)
			a.append(gtk.ScrolledWindow())
			a[4].set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			a[4].add(a[3])
			a.append(filename)
			d = open(filename)
			a[0].set_text(d.read())
			self.window.set_title(os.path.basename(filename) + " - " + os.path.dirname(filename) + " - CodeEDitor")
			self.documents.append(a)
			self.notebook.append_page(self.documents[b][4], gtk.Label(os.path.basename(filename)))
		else:
			print filename + " does not exist"
			gtk.MessageDialog(parent=None, flags=gtk.DIALOG_DESTROY_WITH_PARENT, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format="File not found").show()
			
	def openFile(self):
		fc = gtk.FileChooserDialog(title='Open File...',
									parent=None,
									action=gtk.FILE_CHOOSER_ACTION_OPEN,
									buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		fc.set_default_response(gtk.RESPONSE_OK)
		response = fc.run()
		if response == gtk.RESPONSE_OK:
			self.openPage(fc.get_filename())
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
