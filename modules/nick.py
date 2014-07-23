#
# nick.py - IRC NICK message handler
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
import irc.client

__command__ = 'NICK'
preregister = True

# NICK <nickname> [<hopcount>]
def handle_event(srv, source, params):
	if source in srv.servers.values(): server_nick(srv, source, params)
	else: client_nick(srv, source, params)


def client_nick(srv, source, params):
	if len(params) < 1:
		source.ctcn.numeric(symbols.ERR_NEEDMOREPARAMS, source.nick if hasattr(source, 'nick') else None,
			"NICK : NICK requires at least 1 parameter.")
		return

	target = params[0]

	# can't use nicks already in use
	if target in srv.clients:
		source.ctcn.numeric(symbols.ERR_NICKNAMEINUSE, source.nick if hasattr(source, 'nick') else None,
			"%s :Nick name already in use." % target)
		return
	
	old_nick = source.nick if hasattr(source, 'nick') else None
	
	# change the clients nick
	setattr(source, 'nick', target)
	
	# update the clients registration
	srv.update_client(source, old_nick)
	
	# broadcast the nickname change to everybody
	# (but only if it is a registered client)
	# TODO: make this in-channel only
	if isinstance(source, irc.client.IRCClient):
		srv.announce_common(source, "NICK %s" % target, old_nick)
		
def server_nick(srv, source, params):
	pass
