#
# nick.py
#

import symbols
import irc.client

__command__ = 'NICK'
preregister = True

# NICK <nickname> [<hopcount>]
def handle_event(srv, source, params):
	if len(params) < 1:
		source.ctcn.numeric(symbols.ERR_NEEDMOREPARAMS, source.nick if hasattr(source, 'nick') else None, "NICK : NICK requires at least 1 parameter.")
		return

	target = params[0]

	# can't use nicks already in use
	if target in srv.clients:
		source.ctcn.numeric(symbols.ERR_NICKNAMEINUSE, source.nick if hasattr(source, 'nick') else None, "%s :Nick name already in use." % target)
		return
	
	old_nick = source.nick if hasattr(source, 'nick') else None
	
	# change the clients nick
	setattr(source, 'nick', target)
	
	# update the clients registration
	srv.update_client(source, old_nick)
	
	# broadcast the nickname change to everybody
	# (but only if it is a registered client)
	# TODO: make this in-channel only
	if isinstance(source, irc.client.IRCClient):
		srv.announce_common(source, "NICK %s" % target, old_nick)
