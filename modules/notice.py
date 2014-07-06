#
# privmsg.py
#

import symbols

__command__ = "NOTICE"

def handle_event(srv, ctcn, params):
	if len(params) < 2:
		srv.send_msg(user, "461 %s NOTICE :NOTICE takes at least 2 parameters!" % user.nick)
		return

	target = params[0]
	message = params[1]
	
	if target in srv.channels: # this is a channel message
		# must be a valid channel
		if not target in srv.channels:
			srv.send_msg(user, "403 %s %s :Channel %s doesn't exist." % (ctcn.nick, target, target))
			return
	
		sender = srv.clients[ctcn.nick]
		channel = srv.channels[target]
		
		# can't send external messages in +n channels
		if channel.has_mode('n') and (not sender in channel.members):
			srv.send_msg(ctcn, "404 %s %s :Channel does not recieve outside messages." % (ctcn.nick, target))
			return
		
		print "User's status:", channel.get_status(sender)
		if channel.has_mode('m') and (channel.get_status(sender) < 2**1):
			srv.send_msg(ctcn, "403 %s %s :You must have a voice to send channel messages." % (ctcn.nick, target))
			return
			
		# send the message to the channel
		srv.announce_channel(ctcn, channel, 'NOTICE %s :%s' % (target, message), ctcn.get_hostmask(), exclude = True)
		
	elif target in srv.clients: # this is a PM
		# make sure the target exists
		if not target in srv.clients:
			srv.send_msg(ctcn, "401 %s %s :Nickname not in server database." % (ctcn.nick, nick))
			return
		
		srv.send_msg(srv.clients[target], 'NOTICE %s :%s' % (target, message), ctcn.get_hostmask())
	else:
		return
		
