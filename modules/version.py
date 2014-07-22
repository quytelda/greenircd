#
# version.py - IRC VERSION message handler
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

__command__ = 'VERSION'

def handle_event(srv, source, params):
	# generate the sorted list of modechars and corresponding prefixes
	chan_modes = [symbols.status_modes[x]['modechar'] for x in sorted(symbols.status_modes, reverse=True)]
	chan_prefixes = [symbols.status_modes[x]['prefix'] for x in sorted(symbols.status_modes, reverse=True)]

	# send the expected numeric replies
	source.ctcn.numeric(symbols.RPL_YOURHOST, source.nick,
		':Your host is %s, running version %s' % (srv.name, srv.version))
	source.ctcn.numeric(symbols.RPL_MYINFO, source.nick,
		'%s %s %s %s' % (srv.name, srv.version, ''.join(symbols.user_modes.keys()), ''.join(symbols.chan_modes.keys())))
	source.ctcn.numeric(symbols.RPL_ISUPPORT, source.nick,
		'PREFIX=(%s)%s CHANTYPES=# :are supported' % (''.join(chan_modes), ''.join(chan_prefixes)))
