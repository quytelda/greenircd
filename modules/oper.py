#
# oper.py
#
import os
import hashlib
import json

import symbols

__command__ = 'OPER'

# OPER <username> <password>
def handle_event(srv, user, params):
	if len(params) < 2:
		srv.send_msg(user, "461 %s OPER :OPER takes 2 parameters!" % user.nick)
		return
		
	#if user.has_mode('o'): return # <-- user is already an oper

	username = params[0]
	password = params[1]
	pwdhash = hashlib.sha256(password).hexdigest()
	
	# authenticate the user
	success = False
	if not os.path.isfile('opers.conf'):
		print "* missing file opers.conf"
		return
	
	# find the matching oper entry
	oper_entry = None
	pwdfile = open('opers.conf', 'r')
	for line in pwdfile:
		try:
			entry = json.loads(line)
			if (entry['user'] == username) and (entry['hash'] == pwdhash):
				oper_entry = entry
				break
		except:
			print "* Invalid oper entry:", line
			return
	else: # no matching entries were found
		srv.send_msg(user, "464 %s :Invalid OPER login credentials; this will be reported." % user.nick)
		return
		
	orig_stack = user.mode_stack
	
	# apply the modes listed in the config file
	for flag in oper_entry['flags']:
		if flag in symbols.user_modes:
			user.mode_stack |= symbols.user_modes[flag]
		
	net_modes = "+" + symbols.parse_stack(user.mode_stack ^ orig_stack, symbols.user_modes)
	
	# send the confirmation messages to the user
	srv.send_msg(user, 'MODE %s :+%s' % (user.nick, net_modes))
	srv.send_msg(user, '381 %s :%s' % (user.nick, '*** Logged in as IRC Operator'))
