#
# quit.py
#

__command__ = 'QUIT'

# QUIT (:<reason>)
def handle_event(srv, ctcn, params):
	msg = "Leaving" if (len(params) < 1) else params[0]

	# send announcement, and confirmation
	# must be sent to all channels the user is in
	srv.announce(ctcn, 'QUIT :%s' % msg, ctcn.get_hostmask())

	# remove the user from all channels
	for chan in srv.channels.values():
		if ctcn in chan.members: chan.part(ctcn)
		
	# unregister the user from the server
	if hasattr(ctcn, 'nick') and ctcn.nick in srv.clients:
		del srv.clients[ctcn.nick]
		
	# close the connection
	ctcn.close()
