#
# sendsno.py
#

import symbols

__command__ = "SENDSNO"

def handle_event(srv, source, params):
	if len(params) < 2:
		source.ctcn.message("461 SENDSNO :SENDSNO takes at least 2 parameters!")
		return

	mask = params[0]
	message = params[1]
	
	# send the message to each appropriate client in the server's list
	for client in srv.clients.values():
		if client.has_mode(mask) and (client != source):
			client.ctcn.message("NOTICE %s *** %s" % (client.nick, message))
