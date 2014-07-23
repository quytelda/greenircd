#!/usr/bin/python

# 
#
# main.py - Primary entry point for GreenIRCd software
#
# Copyright (C) 2014 Quytelda Gaiwin <admin@tamalin.org>
#
# This file is part of GreenIRCd, the python IRC daemon.
#
# GreenIRCd is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GreenIRCd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GreenIRCd.  If not, see <http://www.gnu.org/licenses/>.

import os, sys

import server, config

def main(argv):
	fork = True
	path = 'greenircd.conf'
	
	print "Args:", argv
	if '-f' in argv: fork = False
	

	srv = server.Server('green.tamalin.org')
	config.config(srv, path)
	
	if not fork:
		srv.start()
	else:
		# fork the daemon into the background and exit
		try:
			pid = os.fork()
			print "* Forked daemon to background."
		except OSError:
			print "* Failed start background process!"

		if (pid == 0):
			# ungroup the daemon process from the process group
			os.setsid()
			srv.start()

main(sys.argv)
