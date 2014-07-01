#
# topic.py
#

import channel

__command__ = 'TOPIC'

def handle_event(srv, ctcn, params):
	target = params[0]
	channel = srv.channels[target]
	
	if len(params) > 1 and params[1] != '':
		topic = params[1]
		
		# if the channel is +t, only ops can set the topic
		if channel.has_mode('t') and channel.members[ctcn] < 3: return
		
		# apply the change
		channel.topic = topic

		# announce the topic to relevant parties
		srv.announce_channel(ctcn, channel, 'TOPIC %s :%s' % (target, topic), ctcn.get_hostmask())
		
	else: # there were no parameters, so this a query
		
		srv.send_msg(ctcn, '332 %s %s :%s' % (ctcn.nick, target, channel.topic))
