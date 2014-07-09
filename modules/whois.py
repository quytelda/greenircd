#
# nick.py
#

import symbols

__command__ = 'WHOIS'

# WHOIS Syntax: WHOIS [<server>] <nickmask>[,<nickmask>[,...]]
def handle_event(srv, ctcn, params):
	# make sure there are sufficient parameters
	if len(params) < 1:
		srv.send_numeric(ctcn, symbols.ERR_NONICKNAMEGIVEN, "%s WHOIS :The WHOIS command requires one parameter!" % ctcn.nick)
		return
	target = params[0]
	
	# the target must be registered
	if not target in srv.clients:
		srv.send_numeric(ctcn, symbols.ERR_NOSUCHNICK, "%s :Nickname not in server database." % ctcn.nick)
		return
	
	user = srv.clients[target]
	
	cloak = not (ctcn.has_mode('o') or user == ctcn)
	
	# send the information summary
	# TODO: real name, server info
	srv.send_numeric(ctcn, symbols.RPL_WHOISUSER, "%s %s %s * :%s" % (user.nick, user.uid, user.host(cloak), 'REALNAME'))
	srv.send_numeric(ctcn, symbols.RPL_WHOISSERVER, "%s %s :%s" % (user.nick, user.server.name, 'SERVERINFO'))
	
	chans = []
	
	# gather a list of channels to send for the RPL_WHOISCHANNELS message
	# each channel is prefixed with the appropriate status prefix (if applicable)
	for chan in srv.channels:
		if user in srv.channels[chan].members: chans.append(srv.channels[chan].prefix(user)[:1] + chan)
	
	if len(chans) > 0:
		srv.send_numeric(ctcn, symbols.RPL_WHOISCHANNELS, "%s :%s" % (user.nick, ' '.join(chans)))
	
	if user.has_mode('o'):
		srv.send_numeric(ctcn, symbols.RPL_WHOISOPERATOR, "%s :is a server operator [+%s]" % (user.nick, symbols.parse_stack(user.mode_stack, symbols.user_modes)))
	srv.send_numeric(ctcn, symbols.RPL_ENDOFWHOIS, "%s :END OF WHOIS" % user.nick)
