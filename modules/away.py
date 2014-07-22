#
# away.py - IRC AWAY message handler
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

__command__ = 'AWAY'

# Syntax: AWAY [<reason>]
def handle_event(srv, source, params):
	# if a reason is provided, we set away to True
	if len(params) > 0:
		source.away = True
		source.away_reason = params[0]
		source.ctcn.numeric(symbols.RPL_NOWAWAY, source.nick, ":You are now marked as away.")
	elif source.away:
		source.away = False
		source.ctcn.numeric(symbols.RPL_UNAWAY, source.nick, ":You are no longer marked as away.")
