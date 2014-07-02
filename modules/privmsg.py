#
# privmsg.py
#

__command__ = "PRIVMSG"

def handle_event(srv, ctcn, params):
	target = params[0]
	message = params[1]
	
	if target in srv.channels: # this is a channel message
		sender = srv.clients[ctcn.nick]
		channel = srv.channels[target]
		
		# can't send external messages in +n channels
		if channel.has_mode('n') and (not sender in channel.members): return
		
		srv.announce_channel(ctcn, channel, 'PRIVMSG %s :%s' % (target, message), ctcn.get_hostmask(), exclude = True)
	elif target in srv.clients: # this is a PM
		# make sure the target exists
		if not target in srv.clients: return
		
		user = srv.clients[target]
		srv.send_msg(user, 'PRIVMSG %s :%s' % (target, message), ctcn.get_hostmask())
		
