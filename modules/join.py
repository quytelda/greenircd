#
# join.py
# Copyright (C) 2014 Quytelda Gaiwin
#

# TODO: add these responses
# ERR_NEEDMOREPARAMS              ERR_BANNEDFROMCHAN
# ERR_INVITEONLYCHAN              ERR_BADCHANNELKEY
# ERR_BADCHANMASK
#                                 ERR_TOOMANYCHANNELS


from channel import IRCChannel

import symbols
import modules.topic
import modules.names

__command__ = "JOIN"

#
# when a message handled by this modules is encountered, the handle_event method is called
#
def handle_event(srv, source, params):
	# ignore if there are no parameters
	if len(params) < 1: return
	target = params[0]
	
	# targets may be comma separated lists of channels
	# if so, we apply a join to each item in turn
	if ',' in target:
		chans = target.split(',')
		for chan in chans: modules.join.handle_event(srv, source, [chan])
		return

	# channel names must conform to the naming rules
	# TODO allow other prefixes
	if not target.startswith('#'):
		source.ctcn.numeric(symbols.ERR_NOSUCHCHANNEL, source.nick, "%s :No such channel" % target)
		return

	# if we are the first to join the channel, then create it
	if not target in srv.channels:
		srv.channels[target] = IRCChannel(target)
	channel = srv.channels[target]
	
	# if the user is already in the channel, ignore
	if source in channel.members: return
	
	# if the channel has a join limit (+l), and is full, don't join
	# however, operators with override permission can join
	if channel.has_mode('l') and (len(channel.members) >= channel.limit):
		source.ctcn.numeric(symbols.ERR_CHANNELISFULL, source.nick, "%s :Channel is full" % target)
		return
	
	# if the channel is oper only (+O), only server operators can join
	if channel.has_mode('O') and (source.mode_stack < symbols.user_modes['o']):
		srv.send_numeric(ctcn, symbols.ERR_NOPRIVILEGES, ":Only server operators can join.")
		return

	# join the user
	channel.join(source)
	
	print srv.channels.keys()

	# send announcement, and confirmation
	srv.announce_channel(channel, 'JOIN :%s' % target, source.hostmask())

	# generate a NAMES event, so the client will receive a NAMES reply
	modules.names.handle_event(srv, source, [target])

	# send a topic reply to the client
	modules.topic.handle_event(srv, source, [target])
