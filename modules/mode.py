#
# mode.py - IRC MODE message handler
#
# Copyright (C) 2014 Quytelda Gaiwin <admin@tamalin.org>
#
# This file is part of GreenIRCd, the python IRC daemon.
#
# GreenIRCd is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# WeeChat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GreenIRCd.  If not, see <http://www.gnu.org/licenses/>.
import re

import symbols

__command__ = 'MODE'

# MODE Syntax: (:prefix) MODE <target> (+/-)<flags> <params>...
def handle_event(srv, source, params):
	if len(params) < 1:
		source.ctcn.numeric(symbols.ERR_NEEDMOREPARAMS, source.nick, "MODE :MODE requires at least one parameter.")
		return

	target = params[0]

	# the MODE command is handled separately for users and channels
	# so, determine what type of target we are dealing with
	if target in srv.channels:
		channel_mode(srv, source, srv.channels[target], params[1:])
	elif target in srv.clients:
		user_mode(srv, source, srv.clients[target], params[1:])
	else: # the target doesn't exists
		source.ctcn.numeric(symbols.ERR_NOSUCHNICK, source.nick, "%s :No such nick or channel." % target)



def channel_mode(srv, source, channel, params):
	# if only a target is provided,
	# the command is treated as a query
	# TODO add parameters to reply
	if len(params) < 1:
		mode_str = symbols.parse_stack(channel.mode_stack, symbols.chan_modes)
		source.ctcn.numeric(symbols.RPL_CHANNELMODEIS, source.nick, '%s +%s' % (channel.name, mode_str))
		
		# after we've sent the query results, we are done
		return
	
	# if the user is not a channel operator, we can go no further
	# however, if they have override permission, we allow it
	if (channel.members[source] < symbols.CHOPER) and not source.has_mode('Q'): return
	
	# if there more params (a list of flags),
	# we will parse them, and send to the channels
	flags = params[0]
	add_flags = re.sub('\-[a-zA-Z]*', '', flags)[1:] if ('+' in flags) else ''
	rem_flags = re.sub('\+[a-zA-Z]*', '', flags)[1:] if ('-' in flags) else ''
	
	# net_mode accumulates the actual changes applied to the mode
	net_add_flags = '+'
	net_rem_flags = '-'
	tmp_stack = channel.mode_stack

	# add positive mode flags
	for flag in add_flags:
		if (not flag in symbols.chan_modes): continue
		mask = symbols.chan_modes[flag] # get the corresponding mask
		
		# deal with status modes
		# <BEGIN STATUS MODES>
		# (all status modes have a mask of zero, and taking one parameter)
		if (mask == 0) and (len(params) > 1) and (params[1] in srv.clients):
			target = params[1]
			
			# look up the mode
			for status in symbols.status_modes.items():
				if (status[1]['modechar'] == flag) and ((channel.members[source] >= status[0]) or (source.has_mode('o'))):
					channel.members[srv.clients[params[1]]] |= status[0]
					srv.announce_channel(channel, 'MODE %s +%s %s' % (channel.name, flag, params[1]), source.hostmask())
					del params[1]
		# </END STATUS MODES>
		
		# handle the modes that take parameters
		# TODO value checking
		if (flag == 'l') and (len(params) > 1): # Channel limit flag, takes one integer parameter
			channel.limit = int(params[1])
			del params[1]
		elif (flag == 'b') and (len(params) > 1): # Channel ban flag, takes one string parameter
			channel.bans.append(params[1])
		
		# add the mask to the channel mode
		channel.mode_stack |= mask

	# calculate positive mode change
	net_add_flags += symbols.parse_stack(channel.mode_stack ^ tmp_stack, symbols.chan_modes)
	tmp_stack = channel.mode_stack

	# remove negative mode flags
	for flag in rem_flags:
		if not flag in symbols.chan_modes: continue
		mask = symbols.chan_modes[flag] # get the corresponding mask

		# deal with status modes
		if (mask == 0) and (len(params) > 1) and (params[1] in srv.clients):
			target = params[1]

			# look up the mode
			for status in symbols.status_modes.items():
				if (status[1]['modechar'] == flag) and (channel.members[source] >= status[0] or source.has_mode('o')):
					channel.members[srv.clients[params[1]]] ^= status[0]
					srv.announce_channel(channel, 'MODE %s -%s %s' % (channel.name, flag, params[1]), source.hostmask())
					del params[1]

		# subtract the mask from the channel mode
		channel.mode_stack ^= mask

	# calculate negative mode changes
	net_rem_flags += symbols.parse_stack(channel.mode_stack ^ tmp_stack, symbols.chan_modes)
	net_mode = (net_add_flags if (net_add_flags != '+') else '') + (net_rem_flags if (net_rem_flags != '-') else '')

	# if any modes were actually changed, we announce it to the channel
	if len(net_mode) > 0:
		srv.announce_channel(channel, 'MODE %s %s' % (channel.name, net_mode), source.hostmask())



def user_mode(srv, source, user, params):
	# if only a target is provided,
	# the command is treated as a query
	if len(params) < 1:
		modestring = symbols.parse_stack(user.mode_stack, symbols.user_modes)
		if len(modestring) > 0:
			source.ctcn.numeric(symbols.RPL_UMODEIS, source.nick, '+%s' % modestring)
		
		# after we've sent the query results, we are done
		return
	
	# users can only set modes on themselves
	if user.nick != source.nick: return
	
	# if there more params (a list of flags),
	# we will parse them, and send to the channel
	flags = params[0]
	add_flags = re.sub('\-[a-zA-Z]*', '', flags)[1:]
	rem_flags = re.sub('\+[a-zA-Z]*', '', flags)[1:]
	
	net_mode = ''
	tmp_stack = user.mode_stack
	
	for flag in add_flags:
		# operator modes can't be added with the MODE command
		if (not flag in symbols.user_modes): continue
		
		# certain user modes are restricted
		if restricted(source, flag): continue
		
		# apply the mask to the channel mode
		user.mode_stack |= symbols.user_modes[flag]
	
	net_mode += '+' + symbols.parse_stack(user.mode_stack ^ tmp_stack, symbols.user_modes)
	tmp_stack = user.mode_stack
	
	for flag in rem_flags:
		if (not flag in symbols.user_modes): continue
		# apply the mask to the channel mode
		user.mode_stack ^= symbols.user_modes[flag]
		
	net_mode += '-' + symbols.parse_stack(user.mode_stack ^ tmp_stack, symbols.user_modes)
	
	# clean the mode change string by removing extraneous + and -
	net_mode = re.sub(r'\+(?:($|\+|-))', r'\1', net_mode)
	net_mode = re.sub(r'\-+(?:($|\+|-))', r'\1', net_mode)
	
	# send the mode change message
	source.ctcn.message('MODE %s :%s' % (user.nick, net_mode), source.hostmask())



def restricted(user, flag):
	"""Checks to see if manipulation of a mode is restricted for a given user.  If so, it sends an RPL_NOPRIVELEGES numeric and returns true; otherwise, it returns false."""
	# users must use SSL to set +z
	# users must have a vhost
	# reserved for use by services
	if ((flag == 'z') and not user.ctcn.ssl) or \
		((flag == 't') and (user.vhost == None)) or \
		((symbols.user_modes[flag] >= symbols.user_modes['o']) and (user.mode_stack < symbols.user_modes[flag])) or \
		((flag == 'S') or (flag == 'r')):
		user.ctcn.message("481 %s :You don't have the correct priveleges to use this mode." % user.nick)
		return True
	
	return False
