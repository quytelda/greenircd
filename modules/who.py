#
# who.py
#
# TODO this command doesn't see visible (not +i) users who aren't joined in any channel

import symbols

__command__ = 'WHO'

# WHO Syntax: WHO [<name> [<o>]]
# <channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real_name>
def handle_event(srv, source, params):
	
	# if there are no parameters, show all users not marked invisible (+i)
	if len(params) == 0:
		global_who(srv, source)
	if len(params) == 1:
		channel_who(srv, source, srv.channels[params[0]])
	
def global_who(srv, source):
	for channel in srv.channels.values():
		ismem = (source in channel.members)
		for user in channel.members:
			if user.has_mode('i') and (not ismem) and (user != source): continue

			status = ('G' if user.away else 'H') + ('*' if user.has_mode('o') else '') + (channel.prefix(user)[:1])
			source.ctcn.numeric(symbols.RPL_WHOREPLY, source.nick, '%s %s %s %s %s %s :0 %s' % (channel.name, user.username, user.host(), srv.name, user.nick, status, user.real_name))
		
	source.ctcn.numeric(symbols.RPL_ENDOFWHO, source.nick, "* :End of WHO list")
	
def channel_who(srv, source, channel):
	ismem = (source in channel.members)
	for user in channel.members:
		if user.has_mode('i') and (not ismem) and (user != source): continue
		status = ('G' if user.away else 'H') + ('*' if user.has_mode('o') else '') + (channel.prefix(user)[:1])
		source.ctcn.numeric(symbols.RPL_WHOREPLY, source.nick, "%s %s %s %s %s %s :0 %s" % (channel.name, user.username, user.host(), user.server.name, user.nick, status, user.real_name) )
		
	source.ctcn.numeric(symbols.RPL_ENDOFWHO, source.nick, "%s :End of WHO list" % channel.name)
