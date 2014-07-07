#
# join.py
# Copyright (C) 2014 Quytelda Gaiwin
#

# TODO: add these responses
# ERR_NEEDMOREPARAMS              ERR_BANNEDFROMCHAN
# ERR_INVITEONLYCHAN              ERR_BADCHANNELKEY
# ERR_BADCHANMASK
# ERR_NOSUCHCHANNEL               ERR_TOOMANYCHANNELS


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
	
	# targets may be comma separated lists of channels
	# if so, we apply a join to each item in turn
	if ',' in target:
		chans = target.split(',')
		for chan in chans: modules.join.handle_event(srv, ctcn, [chan])
		return

	# if we are the first to join the channel, then create it
	if not (target in srv.channels):
		srv.channels[target] = IRCChannel(target, srv)
	channel = srv.channels[target]
	
	# if the user is already in the channel, ignore
	if ctcn in channel.members: return
	
	# if the channel has a join limit (+l), and is full, don't join
	# however, operators with override permission can join
	if channel.has_mode('l') and (len(channel.members) >= channel.limit):
		srv.send_msg(ctcn, "471 %s %s :Channel is full." % (ctcn.nick, target))
		return

	# join the user
	channel.join(ctcn)

	# send announcement, and confirmation
	srv.announce_channel(ctcn, channel, 'JOIN :%s' % (target), ctcn.get_hostmask())

	# send a name reply to the client
	modules.names.handle_event(srv, ctcn, params)

	# send a topic reply to the client
	modules.topic.handle_event(srv, ctcn, params)
