#
# list.py - IRC LIST message handler
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

__command__ = 'LIST'

# LIST [<channel>{,<channel>} [<server>]]
def handle_event(srv, source, params):
	# send the list header
	source.ctcn.numeric(symbols.RPL_LISTSTART, source.nick, 'Channels :Users Name')
	
	# for each channel send the LIST info
	for channel in srv.channels.values():
		if channel.has_mode('s'): continue
		mode_string = symbols.parse_stack(channel.mode_stack, symbols.chan_modes)
		source.ctcn.numeric(symbols.RPL_LIST, source.nick, '%s %s :[+%s] %s' % (channel.name, len(channel.members), mode_string, channel.topic))
	
	# send the RPL_ENDLIST to signify the finish
	source.ctcn.numeric(symbols.RPL_LISTEND, source.nick, ':End of LIST list')
