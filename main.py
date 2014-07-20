#!/usr/bin/python
# main.py
#
# Copyright (C) 2014 Quytelda Gaiwin

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
			print "* Forking daemon to background."
			pid = os.fork()
		except OSError:
			print "* Failed start background process!"

		if (pid == 0):
			# ungroup the daemon process from the process group
			os.setsid()
			srv.start()

main(sys.argv)
