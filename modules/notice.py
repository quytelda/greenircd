#
# privmsg.py
#

import symbols

__command__ = "NOTICE"

def handle_event(srv, source, params):
	if len(params) < 2:
		source.ctcn.message("461 %s NOTICE :NOTICE takes at least 2 parameters!" % user.nick)
		return

	target = params[0]
	message = params[1]
	
	if target in srv.channels: # this is a channel message
		print "* channel notice", message
		channel = srv.channels[target]
		
		# can't send external messages in +n channels
		if channel.has_mode('n') and (not source in channel.members):
			source.ctcn.message("404 %s %s :Channel does not recieve outside messages." % (source.nick, target))
			return

		if channel.has_mode('m') and (channel.members[source] < symbols.CHVOICE):
			source.ctcn.message("403 %s %s :You must have a voice to send channel messages." % (source.nick, target))
			return
			
		# send the message to the channel
		srv.announce_channel(channel, 'NOTICE %s :%s' % (target, message), source.hostmask(), exclude = True)
		
	elif target in srv.clients: # this is a private notice
		srv.send_msg(srv.clients[target], 'NOTICE %s :%s' % (target, message), source.hostmask())
	else:
		source.ctcn.message("401 %s %s :Not a known nick or channel" % (source.nick, target))
		
