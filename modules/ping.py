#
# ping.py - IRC PING message handler
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

def handle_event(srv, source, params):
	
	# for clients, return a pong simple
	# :prefix PONG <servername> :<token>
	if source in srv.clients.values():
		token = params[0] if (len(params) > 0) else srv.name
		source.ctcn.message("PONG %s :%s" % (srv.name, token))
