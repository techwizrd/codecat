#!/usr/bin/env python
#
#		ced.py
#
#		Copyright 2009 techwizrd <theninja@Bluedevs.net>
#
#		This program is free software; you can redistribute it and/or modify
#		it under the terms of the GNU General Public License as published by
#		the Free Software Foundation; either version 2 of the License, or
#		(at your option) any later version.
#
#		This program is distributed in the hope that it will be useful,
#		but WITHOUT ANY WARRANTY; without even the implied warranty of
#		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#		GNU General Public License for more details.
#
#		You should have received a copy of the GNU General Public License
#		along with this program; if not, write to the Free Software
#		Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#		MA 02110-1301, USA.

import sys

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
	print "PyGTK not found!"
	sys.exit(1)
try:
	import gtk
	import gtksourceview
	import mimetypes
	import os
except ImportError, e:
	print "%s found!" % e
	sys.exit(1)
except Exception, e:
	print str(e)
	sys.exit(1)

if __name__ == "__main__":
