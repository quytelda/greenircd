#
# chghost.py
# Copyright (C) Quytelda Gaiwin
#
# TODO make sure the new host is a valid host (can't contain special characters, etc)

import symbols

import modules.mode

__command__ = 'CHGHOST'

# Syntax: CHGHOST <nick> <new host>
def handle_event(srv, source, params):
	if len(params) < 2:
		source.ctcn.message("461 %s CHGHOST :CHGHOST takes at least 2 parameters!" % source.nick)
		return

	# only operators can use CHGHOST
	if not source.has_mode('o'):
		source.ctcn.message("481 %s :You must be a server operator." % source.nick)
		return

	target = params[0]
	new_host = params[1]

	# if the target doesn't exist, send a 401 and exit
	if not target in srv.clients:
		source.ctcn.message("401 %s :Nickname not in server database." % source.nick)
		return

	user = srv.clients[target]

	# set the vhost and add the +t flag
	user.vhost = new_host
	modules.mode.handle_event(srv, source, [source.nick, '+t'])
	
	source.ctcn.message("NOTICE %s :Changed vhost to %s." % (source.nick, new_host))
