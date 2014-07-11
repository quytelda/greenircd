#
# who.py
#

import symbols

__command__ = 'WHO'

# WHO Syntax: WHO [<name> [<o>]]
# <channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real_name>
def handle_event(srv, ctcn, params):
	
	# if there are no parameters, show all users not marked invisible (+i)
	if len(params) == 0:
		global_who(srv, ctcn, params)
	if len(params) == 1:
		channel_who(srv, ctcn, srv.channels[params[0]])
	
def global_who(srv, ctcn, params):
	for channel in srv.channels.values():
		ismem = (ctcn in channel.members)
		for user in channel.members:
			if user.has_mode('i') and not ismem: continue
		
			srv.send_numeric(ctcn, symbols.RPL_WHOREPLY, '%s %s %s %s %s %s :0 %s' % (channel.name, user.uid, user.host(), srv.name, user.nick, 'H', 'REALNAME'))
		
	srv.send_numeric(ctcn, symbols.RPL_ENDOFWHO, "* :End of WHO list")
	
def channel_who(srv, ctcn, channel):
	for user in channel.members:
		srv.send_numeric(ctcn, symbols.RPL_WHOREPLY, "%s %s %s %s %s %s :0 REALNAME" % (channel.name, user.uid, user.host(), user.server.name, user.nick, 'H') )
		
	srv.send_numeric(ctcn, symbols.RPL_ENDOFWHO, "%s :End of /WHO list." % channel.name)
