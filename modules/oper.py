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
		
	if user.has_mode('o'): return # <-- user is already an oper

	username = params[0]
	password = params[1]
	pwdhash = hashlib.sha256(password).hexdigest()
	
	# authenticate the user
	success = False
	if not os.path.isfile('opers.conf'):
		print "* missing file opers.conf"
		return
		
	pwdfile = open('opers.conf', 'r')
	for line in pwdfile:
		try:
			entry = json.loads(line)
			success = (entry['user'] == username) and (entry['hash'] == pwdhash)
			if success: break
		except:
			print "* Invalid oper entry:", line
			continue
	else: # no matching entries were found
		srv.send_msg(user, "464 %s :Invalid OPER login credentials; this will be reported." % user.nick)
		return
	
	# add the appropriate modes
	for flag in symbols.oper_modes:
		user.mode_stack |= symbols.user_modes[flag]
	
	srv.send_msg(user, 'MODE %s :+%s' % (user.nick, symbols.oper_modes), user.nick)
	srv.send_msg(user, '381 %s :%s' % (user.nick, '*** Logged in as IRC Operator'))
