#
# sendsno.py - IRC SENDSNO message handler
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

__command__ = "SENDSNO"

def handle_event(srv, source, params):
	if len(params) < 2:
		source.ctcn.message("461 SENDSNO :SENDSNO takes at least 2 parameters!")
		return

	mask = params[0]
	message = params[1]
	
	# send the message to each appropriate client in the server's list
	for client in srv.clients.values():
		if client.has_mode(mask) and (client != source):
			client.ctcn.message("NOTICE %s *** %s" % (client.nick, message))
