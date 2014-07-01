#
# join.py
#

from channel import IRCChannel

import modules.topic
import modules.names

__command__ = "JOIN"

#
# when a message handled by this modules is encountered, the handle_event method is called
#
def handle_event(srv, ctcn, params):
	# die if there are no parameters
	if len(params) < 1: return
	target = params[0]

	if not (target in srv.channels): # we are the first to join the channel, create it
		srv.channels[target] = IRCChannel(target, srv)
	channel = srv.channels[target]
	
	# if the user is already in the channel, ignore
	if ctcn in channel.members: return

	# join the user
	channel.join(ctcn)

	# send announcement, and confirmation
	srv.announce_channel(ctcn, channel, 'JOIN :%s' % (target), ctcn.get_hostmask())

	# send a name reply to the client
	modules.names.handle_event(srv, ctcn, params)

	# send a topic reply to the client
	modules.topic.handle_event(srv, ctcn, params)
