#
# kick.py - IRC KICK message handler
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

from channel import IRCChannel

import symbols
import modules.names

__command__ = "KICK"

# (:prefix) KICK <#target> <user> (:reason)
def handle_event(srv, source, params):
	if len(params) < 2:
		source.ctcn.message("461 %s KICK :KICK takes at least 2 parameters!" % source.nick)
		return
	
	target = params[0]
	nick = params[1]
	reason = params[2] if (len(params) > 2) else source.nick
	
	# must be a valid channel
	if not target in srv.channels:
		source.ctcn.message("403 %s %s :Channel %s doesn't exist." % (source.nick, target, target))
		return
	channel = srv.channels[target]
	
	# user must be a valid user
	if not nick in srv.clients:
		source.ctcn.message("401 %s %s :Nickname not in server database." % (source.nick, nick))
		return
	user = srv.clients[nick]
	
	# can't kick users who are protected (have +q usermode)
	if user.has_mode('q'):
		source.ctcn.message("481 %s :Can't kick protected users." % source.nick)
		return
	
	# user must already be in the channel
	if not user in channel.members:
		source.ctcn.message("482 %s %s :User is not in channel." % (source.nick, target))
		return
	user_status = channel.members[user]
	
	# only channel operators can kick
	# however, users with override permission are allowed to kick without becoming chanops
	if (not source in channel.members) or ((channel.members[source] < symbols.CHOPER) and not source.has_mode('Q')):
		source.ctcn.message("482 %s %s :You must be a channel operator to use KICK." % (source.nick, target))
		return

	# can't kick someone with higher access level
	if channel.members[user] >= channel.members[source]: return
	
	# apply the kick
	srv.announce_channel(channel, 'KICK %s %s :%s' % (target, nick, reason), source.hostmask())
	channel.part(user)
	
	
