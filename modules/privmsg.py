#
# privmsg.py - IRC PRIVMSG message handler
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
# GreenIRCd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GreenIRCd.  If not, see <http://www.gnu.org/licenses/>.

import symbols

__command__ = "PRIVMSG"

def handle_event(srv, source, params):
	if len(params) < 2:
		source.ctcn.notice(symbols.ERR_NEEDMOREPARAMS, source.nick, "PRIVMSG :PRIVMSG takes at least 2 parameters!")
		return

	target = params[0]
	message = params[1]

	if target in srv.clients:
		user = srv.clients[target]
		user.ctcn.message("PRIVMSG %s :%s" % (target, message), source.hostmask())
	elif target in srv.channels:
		channel = srv.channels[target]

		# can't send external messages in +n channels
		if channel.has_mode('n') and (not source in channel.members):
			source.ctcn.numeric(symbols.ERR_CANNOTSENDTOCHAN, source.nick, "%s :Channel does not recieve outside messages." % target)
			return

		if channel.has_mode('m') and (channel.members[source] < symbols.CHVOICE):
			source.ctcn.numeric(symbols.ERR_CANNOTSENDTOCHAN, source.nick, "%s :You must have a voice to send channel messages." % target)
			return

		srv.announce_channel(channel, "PRIVMSG %s :%s" % (target, message), source.hostmask(), exclude = source)
	else:
		source.ctcn.numeric(symbols.ERR_NOSUCHNICK, source.nick, "%s :No such nick or channel" % target)
