#
# mode.py
# Copyright (C) 2014 Quytelda Gaiwin
#
import re

import symbols

__command__ = 'MODE'

# (:prefix) MODE <target> (+/-)<flags> <params>...

def handle_event(srv, ctcn, params):
	if len(params) < 1:
		srv.send_msg(user, "461 %s MODE :MODE takes at least 1 parameter!" % user.nick)
		return

	target = params[0]

	# the MODE command is handled separately for users and channels
	# so, determine what type of target we are dealing with
	if target in srv.channels:
		channel_mode(srv, ctcn, srv.channels[target], params[1:])
	elif target in srv.clients:
		user_mode(srv, ctcn, srv.clients[target], params[1:])
	else: # the target doesn't exists
		srv.send_msg(ctcn, "401 %s :%s is not a known nick or channel!" % (target, target))

def channel_mode(srv, ctcn, channel, params):
	# if only a target is provided,
	# the command is treated as a query
	if (len(params) < 1) or (params[0] == ''):
		mode_str = symbols.parse_stack(channel.mode_stack, symbols.chan_modes)
		srv.send_msg(ctcn, '324 %s %s +%s' % (ctcn.nick, channel.name, mode_str))
		
		# after we've sent the query results, we are done
		return
	
	# if the user is not a channel operator, we can go no further
	if channel.members[ctcn] < 2**3 and not ctcn.has_mode('o'): return
	
	# if there more params (a list of flags),
	# we will parse them, and send to the channels
	flags = params[0]
	add_flags = re.sub('\-[a-zA-Z]*', '', flags)[1:]
	rem_flags = re.sub('\+[a-zA-Z]*', '', flags)[1:]
	
	# net_mode accumulates the actual changes applied to the mode
	net_mode = ''
	tmp_stack = channel.mode_stack
	
	for flag in add_flags:
		if not flag in symbols.chan_modes: continue
		channel.add_mode(flag, params[1:])
	
	net_mode += '+' + symbols.parse_stack(channel.mode_stack ^ tmp_stack, symbols.chan_modes)
	tmp_stack = channel.mode_stack	
	
	for flag in rem_flags:
		if not flag in symbols.chan_modes: return
		channel.rem_mode(flag, params[1:])
		
	net_mode += '-' + symbols.parse_stack(channel.mode_stack ^ tmp_stack, symbols.chan_modes)
		
	srv.announce_channel(ctcn, channel, 'MODE %s %s' % (channel.name, ' '.join(params)), ctcn.get_hostmask())
		
def user_mode(srv, ctcn, user, params):
	# if only a target is provided,
	# the command is treated as a query
	if (len(params) < 1) or (params[0] == ''):
		modestring = symbols.parse_stack(user.mode_stack, symbols.user_modes)
		srv.send_msg(ctcn, '221 %s +%s' % (user.nick, modestring))
		
		# after we've sent the query results, we are done
		return
	
	# users can only set modes on themselves
	if user.nick != ctcn.nick: return
	
	# if there more params (a list of flags),
	# we will parse them, and send to the channel
	flags = params[0]
	add_flags = re.sub('\-[a-zA-Z]*', '', flags)[1:]
	rem_flags = re.sub('\+[a-zA-Z]*', '', flags)[1:]
	
	net_mode = ''
	tmp_stack = user.mode_stack
	
	for flag in add_flags:
		# operator modes can't be added with the MODE command
		if symbols.user_modes[flag] >= symbols.user_modes['o']: continue
		
		# apply the mask to the channel mode
		user.mode_stack |= symbols.user_modes[flag]
	
	net_mode += '+' + symbols.parse_stack(user.mode_stack ^ tmp_stack, symbols.user_modes)
	tmp_stack = user.mode_stack
	
	for flag in rem_flags:
		# apply the mask to the channel mode
		user.mode_stack ^= symbols.user_modes[flag]
		
	net_mode += '-' + symbols.parse_stack(user.mode_stack ^ tmp_stack, symbols.user_modes)
		
	#stack_diff = user.mode_stack ^ initial_stack
	#print "* stack_diff:", symbols.parse_stack(stack_diff, symbols.user_modes)
		
	srv.send_msg(ctcn, 'MODE %s :%s' % (user.nick, net_mode), ctcn.get_hostmask())
