#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class Ced:
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.show()
	
	def main(self):
		gtk.main()

print __name__
if __name__ == "__main__":
	CedWin = Ced()
	CedWin.main()
