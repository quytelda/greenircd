#
# part.py - IRC PART message handler
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

import mode

__command__ = 'PART'

def handle_event(srv, source, params):
	# die if there are no parameters
	if len(params) < 1:
		source.ctcn.numeric(symbols.ERR_NEEDMOREPARAMS, source.nick, "PART :PART takes at least 1 parameters!")
		return

	target = params[0]
	msg = "Leaving" if (len(params) < 2) else params[1]

	# if the channel doesn't exist, ignore
	if not (target in srv.channels):
		return

	channel = srv.channels[target]

	# if the user is not in the channel, ignore
	if not source in channel.members: return

	# send announcement, and confirmation
	srv.announce_channel(channel, 'PART %s :%s' % (target, msg), source.hostmask())

	# part the user
	channel.part(source)
	
	# if that was the last user in the channel, we should forget the channel
	# TODO
