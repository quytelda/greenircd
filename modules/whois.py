#
# nick.py
#

import symbols

__command__ = 'WHOIS'

# WHOIS Syntax: WHOIS [<server>] <nickmask>[,<nickmask>[,...]]
def handle_event(srv, source, params):
	# make sure there are sufficient parameters
	if len(params) < 1:
		source.ctcn.numeric(symbols.ERR_NONICKNAMEGIVEN, source.nick, "%s WHOIS :The WHOIS command requires one parameter!" % source.nick)
		return
	target = params[0]
	
	# the target must be registered
	if not target in srv.clients:
		source.ctcn.numeric(symbols.ERR_NOSUCHNICK, source.nick, "%s :Nickname not in server database." % source.nick)
		return
	
	user = srv.clients[target]
	
	cloak = not (source.has_mode('o') or user == source)
	
	# send the information summary
	# TODO: real name, server info
	source.ctcn.numeric(symbols.RPL_WHOISUSER, source.nick, "%s %s %s * :%s" % (user.nick, user.username, user.host(cloak), user.real_name))
	source.ctcn.numeric(symbols.RPL_WHOISSERVER, source.nick, "%s %s :%s" % (user.nick, user.server.name, srv.info))
	
	chans = []
	
	# gather a list of channels to send for the RPL_WHOISCHANNELS message
	# each channel is prefixed with the appropriate status prefix (if applicable)
	for chan in srv.channels:
		if user in srv.channels[chan].members: chans.append(srv.channels[chan].prefix(user)[:1] + chan)
	
	if len(chans) > 0:
		source.ctcn.numeric(symbols.RPL_WHOISCHANNELS, source.nick, "%s :%s" % (user.nick, ' '.join(chans)))
	
	if user.has_mode('o'):
		source.ctcn.numeric(symbols.RPL_WHOISOPERATOR, source.nick, "%s :is a server operator [+%s]" % (user.nick, symbols.parse_stack(user.mode_stack, symbols.user_modes)))
	source.ctcn.numeric(symbols.RPL_ENDOFWHOIS, source.nick, "%s :END OF WHOIS" % user.nick)
