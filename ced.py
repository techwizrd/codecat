#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, gtksourceview, mimetypes

class Ced:
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.documents = []
		self.vbox = gtk.VBox(homogeneous = False, spacing = 0)
		self.notebook = gtk.Notebook()
		self.vbox.add(self.notebook)
		self.window.resize(800,600)
		self.window.add(self.vbox)
		self.newPage("./ced.py")
		self.window.show_all()

	def delete_event(widget, event, data=None):
		print "delete event occurred"
		return False

	def destroy(widget, data=None):
		print "destroy signal occurred"
		gtk.main_quit()

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

	def newPage(self, filename):
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
		self.window.set_title(a[5] + " - CodeEDitor")
		self.documents.append(a)
		self.notebook.append_page(self.documents[b][4], gtk.Label(filename))


	def main(self):
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		gtk.main()


print __name__
if __name__ == "__main__":
	CedWin = Ced()
	CedWin.main()
