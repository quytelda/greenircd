#!/usr/bin/python
# main.py
#
# Copyright (C) 2014 Quytelda Gaiwin

import server
import config

def main(path):
	srv = server.Server('green.tamalin.org')
	config.config(srv, path)
	srv.start()

main('greenircd.conf')
