#
# privmsg.py
#

__command__ = "PRIVMSG"

def handle_event(srv, ctcn, params):
	target = params[0]
	message = params[1]
	
	if (target in srv.channels): # this is a channel message
		channel = srv.channels[target]
		srv.announce_channel(ctcn, channel, 'PRIVMSG %s :%s' % (target, message), ctcn.get_hostmask(), exclude = True)
