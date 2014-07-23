#
# chghost.py - IRC CHGHOST message handler
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
# TODO make sure the new host is a valid host (can't contain special characters, etc)

import symbols

__command__ = 'CHGHOST'

# Syntax: CHGHOST <nick> <new host>
def handle_event(srv, source, params):
	if len(params) < 2:
		source.ctcn.message("461 %s CHGHOST :CHGHOST takes at least 2 parameters!" % source.nick)
		return

	# only operators can use CHGHOST
	if not source.has_mode('o'):
		source.ctcn.message("481 %s :You must be a server operator." % source.nick)
		return

	target = params[0]
	new_host = params[1]

	# if the target doesn't exist, send a 401 and exit
	if not target in srv.clients:
		source.ctcn.message("401 %s :Nickname not in server database." % source.nick)
		return

	user = srv.clients[target]

	# set the vhost and add the +t flag
	user.vhost = new_host
	user.mode_stack |= symbols.user_modes['t']
	source.ctcn.message("MODE %s :+t" % user.nick, source.hostmask())
	
	source.ctcn.message("NOTICE %s :Changed vhost to %s." % (source.nick, new_host))
