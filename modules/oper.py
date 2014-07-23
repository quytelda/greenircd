#
# oper.py - IRC OPER message handler
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

import os
import hashlib

import symbols
import modules.join
import modules.sendsno

__command__ = 'OPER'

# OPER <username> <password>
def handle_event(srv, user, params):
	if len(params) < 2:
		user.ctcn.message("461 %s OPER :OPER takes 2 parameters!" % user.nick)
		return

	username = params[0]
	password = params[1]
	
	pwdhash = hashlib.sha256(password).hexdigest()
	modelist = None
	
	# authenticate the user
	for oper in srv.opers:
		if (oper['username'] == username) and (oper['auth'] == pwdhash):
			# if there are flags in the oper entry, remember them for later
			modelist = oper['flags']
			break
	else: # no matching entries were found
		user.ctcn.message("464 %s :Invalid OPER login credentials; this will be reported." % user.nick)
		return

	orig_stack = user.mode_stack

	# apply the modes listed in the config file
	for flag in modelist:
		if flag in symbols.user_modes:
			user.mode_stack |= symbols.user_modes[flag]

	net_modes = "+" + symbols.parse_stack(user.mode_stack ^ orig_stack, symbols.user_modes)

	# send the confirmation messages to the user
	user.ctcn.message('MODE %s :%s' % (user.nick, net_modes), user.hostmask())
	user.ctcn.message('381 %s :%s' % (user.nick, '*** Logged in as IRC Operator ***'))
	modules.sendsno.handle_event(srv, user, ['s', 'Notice: Oper-up by %s.' % user.hostmask()])

	# if there are channels for opers to autojoin, join them
	if len(srv.operjoin) > 0:
		modules.join.handle_event(srv, user, [srv.operjoin])
