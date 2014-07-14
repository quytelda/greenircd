#
# kill.py
# Copyright (C) Quytelda Gaiwin
#

import symbols

import config

__command__ = 'REHASH'

def handle_event(srv, source, params):
	# only operators can use REHASH
	if not source.has_mode('o'):
		source.ctcn.message("481 %s :You must be a server operator." % source.nick)
		return

	# announce the rehash
	# TODO what is XXX supposed to be?
	source.ctcn.numeric(symbols.RPL_REHASHING, source.nick, "%s :Rehashing config file..." % srv.config)
	config.config(srv, srv.config)
	source.ctcn.numeric(symbols.RPL_REHASHING, source.nick, "%s :Sucessfully rehashed %s" % (srv.config, srv.name))
