#
# quit.py
#
import irc.client

__command__ = 'QUIT'
preregister = True

# QUIT (:<reason>)
def handle_event(srv, source, params):
	"""
	QUIT terminates a client connection, with an optional message.
	The QUIT will be announced to all channels the user is in, and if the user
	is registered, it will be unregistered from the server.
	Closing of the actual socket occurs last (after the client is unregistered).
	A quite event triggers an unregistration.
	"""
	msg = params[0] if len(params)> 0 else (source.nick if hasattr(source, 'nick') else '')

	# announce the quit event
	# TODO make this in-channel
	if source in srv.clients.values():
		srv.announce("QUIT :%s" % msg, source.hostmask())

	# remove the user from all channels
	for channel in srv.channels.values():
		if source in channel.members: channel.part(source)
		
	# unregister the user from the server
	if isinstance(source, irc.client.IRCClient) and (source.nick in srv.clients): # the user is registered currently
		srv.unregister_client(source)

	# close the connection
	source.terminate()
