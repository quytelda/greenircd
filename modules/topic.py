#
# topic.py
#

import symbols
import channel

__command__ = 'TOPIC'

def handle_event(srv, source, params):
	if len(params) < 1:
		source.ctcn.numeric(symbols.ERR_NEEDMOREPARAMS, source.nick, "TOPIC :TOPIC requires at least one parameter.")
		return

	target = params[0]
	
	# the channel must exist
	if not target in srv.channels:
		source.ctcn.numeric(symbols.ERR_NOSUCHCHANNEL, source.nick, "%s :No such channel." % target)
		return
	channel = srv.channels[target]
	
	# if there are no other parameters, this is a query
	if len(params) < 2:
		source.ctcn.numeric(symbols.RPL_TOPIC, source.nick, '%s :%s' % (target, channel.topic))
	else:
		topic = params[1]
		
		# if the channel is +t, only ops and higher can set the topic
		if channel.has_mode('t') and channel.members[source] < symbols.CHOPER: return
		
		# apply the change
		channel.topic = topic

		# announce the topic to relevant parties
		srv.announce_channel(channel, 'TOPIC %s :%s' % (target, topic), source.hostmask())
