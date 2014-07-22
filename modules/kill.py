#
# kill.py - IRC KILL message handler
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

import modules.quit

__command__ = 'KILL'

def handle_event(srv, source, params):
	if len(params) < 1:
		source.ctcn.message("461 %s KILL :KILL takes at least 1 parameter!" % source.nick)
		return

	# only operators can use KILL
	if not source.has_mode('o'):
		source.ctcn.message("481 %s :You must be a server operator." % source.nick)
		return

	target = params[0]
	reason = params[1] if (len(params) > 1) else source.nick

	# if the target doesn't exist, send a 401 and exit
	if not target in srv.clients:
		source.ctcn.message("401 %s :Nickname not in server database." % source.nick)
		return

	user = srv.clients[target]

	# can't kill protected users unless you have sufficient status
	if user.has_mode('q') and (source.mode_stack < symbols.user_modes['q']):
		source.ctcn.message("481 %s :You don't have permission to kill protected users." % source.nick)
		return

	# announce the kill notice
	# TODO what is XXX supposed to be?
	source.ctcn.message("KILL %s :XXX %s" % (user.nick, reason), source.hostmask())

	# create a quit event
	modules.quit.handle_event(srv, user, ['[%s] Local kill by %s (%s)' % (srv.name, source.nick, reason)])
