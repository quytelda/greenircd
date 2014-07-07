#
# who.py
#

import symbols

__command__ = 'WHO'

# <channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real_name>
def handle_event(srv, ctcn, params):
	# if there are no params, this is a global query
	# TODO: implement globals
	if len(params) < 1:
		for chan in srv.channels:
			channel_who(srv, ctcn, srv.channels[chan])
	elif params[0] in srv.channels:
		channel_who(srv, ctcn, srv.channels[params[0]])

def channel_who(srv, ctcn, channel, params = []):
	# if there is one query, it is probably by a channel
	
	for member in channel.members:
		chan_status = channel.get_status(member)
		status = 'H' + symbols.status_modes[chan_status]['prefix']
		if member.has_mode('o'): status += '*'

		cloak = False if ctcn.has_mode('o') else True

		srv.send_msg(ctcn, '352 %s %s %s %s %s %s %s :0 %s' % (member.nick, channel.name, member.uid, member.host(cloak), srv.name, member.nick, status, 'REALNAME'))

	srv.send_msg(ctcn, '315 %s %s :%s' % (ctcn.nick, channel.name, "End of /WHO List"))
