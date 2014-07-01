#
# who.py
#

import symbols

__command__ = 'WHO'

def handle_event(srv, ctcn, params):
	channel = params[0]
	
	
	for member in srv.channels[channel].members:
		chan_status = srv.channels[channel].members[member]
		status = 'H' + symbols.chan_status_modes[chan_status]['prefix'];

		srv.send_msg(ctcn, '352 %s %s %s %s %s %s %s :0 %s' % (ctcn.nick, channel, ctcn.uid, ctcn.transport.getPeer().host, srv.name, ctcn.nick, status, 'REALNAME'))

	srv.send_msg(ctcn, '315 %s %s :%s' % (ctcn.nick, channel, "End of /WHO List"))
