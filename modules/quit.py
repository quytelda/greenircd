#
# quit.py - IRC QUIT message handler
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

import irc.client

__command__ = 'QUIT'
preregister = True

# QUIT (:<reason>)
def handle_event(srv, source, params):
	"""
	QUIT terminates a client connection, with an optional message.
	The QUIT will be announced to all channels the user is in, and if the user
	is registered, it will be unregistered from the server.
	Closing of the actual socket occurs last (after the client is unregistered).
	A quite event triggers an unregistration.
	"""
	msg = params[0] if len(params)> 0 else (source.nick if hasattr(source, 'nick') else '')

	# announce the quit event
	# TODO make this in-channel
	if source in srv.clients.values():
		srv.announce("QUIT :%s" % msg, source.hostmask())

	# remove the user from all channels
	for channel in srv.channels.values():
		if source in channel.members: channel.part(source)
		
	# unregister the user from the server
	if isinstance(source, irc.client.IRCClient) and (source.nick in srv.clients): # the user is registered currently
		srv.unregister_client(source)

	# close the connection
	source.terminate()
