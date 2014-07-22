#
# user.py - IRC USER message handler
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

from irc.client import IRCClient

__command__ = 'USER'
preregister = True

# USER <username> <hostname> <servername> :<realname>
def handle_event(srv, source, params):
	if len(params) > 4:
		source.ctcn.numeric(symbols.ERR_ALREADYREGISTERED, None, "USER :User takes four parameters!")

	# users can only register once
	if hasattr(source, 'nick') and (source.nick in srv.clients):
		source.ctcn.numeric(symbols.ERR_ALREADYREGISTERED, None, ":You are already registered!")

	username = params[0]
	hostname = params[1]
	server = params[2]
	realname = params[3]

	# the user command tells us that we have a client connecting, not a server
	# if the connection is still in an IRCConnection (generic) container, put it in
	# an IRCClient container and try to register it with the server
	nick = source.nick if hasattr(source, 'nick') else None
	client = IRCClient(srv, source.ctcn, username, nick)
	client.real_name = realname
	srv.register_client(client)
