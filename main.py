#!/usr/bin/python
# main.py
#
# Copyright (C) 2014 Quytelda Gaiwin

import server

def main(path):
	srv = server.Server('green.tamalin.org')
	srv.start()

main('greenircd.conf')
