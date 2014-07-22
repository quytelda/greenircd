#
# notice.py - IRC NOTICE message handler
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

import symbols

__command__ = "NOTICE"

def handle_event(srv, source, params):
	if len(params) < 2:
		source.ctcn.message("461 %s NOTICE :NOTICE takes at least 2 parameters!" % user.nick)
		return

	target = params[0]
	message = params[1]
	
	if target in srv.channels: # this is a channel message
		channel = srv.channels[target]
		
		# can't send external messages in +n channels
		if channel.has_mode('n') and (not source in channel.members):
			source.ctcn.message("404 %s %s :Channel does not recieve outside messages." % (source.nick, target))
			return

		if channel.has_mode('m') and (channel.members[source] < symbols.CHVOICE):
			source.ctcn.message("403 %s %s :You must have a voice to send channel messages." % (source.nick, target))
			return
			
		# send the message to the channel
		srv.announce_channel(channel, 'NOTICE %s :%s' % (target, message), source.hostmask(), exclude = True)
		
	elif target in srv.clients: # this is a private notice
		user = srv.clients[target]
		user.ctcn.message('NOTICE %s :%s' % (target, message), source.hostmask())
	else:
		source.ctcn.message("401 %s %s :Not a known nick or channel" % (source.nick, target))
		
