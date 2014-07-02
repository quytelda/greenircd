#
# who.py
#

import symbols

__command__ = 'WHO'

# <channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real_name>
def handle_event(srv, ctcn, params):
	# if there are no params, this is a global query
	# TODO: implement globals
	if len(params) < 1: return

	# if there is one query, it is probably by a channel
	target = params[0]
	channel = srv.channels[target]
	
	for member in channel.members:
		chan_status = channel.get_status(member)
		status = 'H' + symbols.status_modes[chan_status]['prefix'];

		srv.send_msg(ctcn, '352 %s %s %s %s %s %s %s :0 %s' % (ctcn.nick, target, ctcn.uid, ctcn.transport.getPeer().host, srv.name, ctcn.nick, status, 'REALNAME'))

	srv.send_msg(ctcn, '315 %s %s :%s' % (ctcn.nick, target, "End of /WHO List"))
