#
# join.py - IRC JOIN message handler
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
		srv.channels[target] = IRCChannel(target, srv)
	channel = srv.channels[target]

	# if the user is already in the channel, ignore
	if source in channel.members: return
	
	# if the channel has a join limit (+l), and is full, don't join
	# however, operators with override permission can join
	if channel.has_mode('l') and (len(channel.members) >= channel.limit):
		source.ctcn.numeric(symbols.ERR_CHANNELISFULL, source.nick, "%s :Channel is full" % target)
		return

	# if the channel is oper only (+Z), only ssl clients can join
	if channel.has_mode('Z') and not source.has_mode('z'):
		source.ctcn.numeric(symbols.ERR_NOPRIVILEGES, source.nick, ":You must be connected with SSL.")
		return

	# if the channel is oper only (+O), only server operators can join
	if channel.has_mode('O') and (source.mode_stack < symbols.user_modes['o']):
		source.ctcn.numeric(symbols.ERR_NOPRIVILEGES, source.nick, ":Only server operators can join.")
		return
		
	# if the channel is oper only (+A), only server admins can join
	if channel.has_mode('A') and (source.mode_stack < symbols.user_modes['a']):
		source.ctcn.numeric(symbols.ERR_NOPRIVILEGES, source.nick, ":Only server administrators can join.")
		return

	# join the user
	channel.join(source)

	# send announcement, and confirmation
	srv.announce_channel(channel, 'JOIN :%s' % target, source.hostmask())

	# generate a NAMES event, so the client will receive a NAMES reply
	modules.names.handle_event(srv, source, [target])

	# send a topic reply to the client
	modules.topic.handle_event(srv, source, [target])
