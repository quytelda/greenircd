#
# user.py
#

import symbols

from irc.client import IRCClient

__command__ = 'USER'
preregister = True

# USER <username> <hostname> <servername> :<realname>
def handle_event(srv, source, params):
	# users can only register once
	if hasattr(source, 'nick') and (source.nick in srv.clients):
		source.ctcn.numeric(symbols.ERR_ALREADYREGISTERED, ":You are already registered!", source.nick)

	username = params[0]
	#hostname = params[1]
	#server = params[2]
	#realname = params[3]

	# the user command tells us that we have a client connecting, not a server
	# if the connection is still in an IRCConnection (generic) container, put it in
	# an IRCClient container and try to register it with the server
	nick = source.nick if hasattr(source, 'nick') else None
	client = IRCClient(srv, source.ctcn, username, nick)
	srv.register_client(client)
	
	print srv.clients
	print client.nick, client.username
