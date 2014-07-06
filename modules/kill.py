#
# kill.py
# Copyright (C) Quytelda Gaiwin
#

import symbols

import modules.quit

__command__ = 'KILL'

def handle_event(srv, ctcn, params):
	if len(params) < 1:
		srv.send_msg(ctcn, "461 %s KILL :KILL takes at least 1 parameter!" % ctcn.nick)
		return
	
	# only operators can use KILL
	if not ctcn.has_mode('o'):
		srv.send_msg(ctcn, "481 %s :You must be a server operator." % ctcn.nick)
		return
	
	target = params[0]
	reason = params[1] if (len(params) > 1) else ctcn.nick
	
	# if the target doesn't exist, send a 401 and exit
	if not target in srv.clients:
		srv.send_msg(ctcn, "401 %s :Nickname not in server database." % ctcn.nick)
		return
	
	user = srv.clients[target]
	
	# can't kill protected users unless you have sufficient status
	if user.has_mode('q') and (ctcn.mode_stack < symbols.user_modes['q']):
		srv.send_msg(ctcn, "481 %s :You don't have permission to kill protected users." % ctcn.nick)
		return
	
	# announce the kill notice
	# TODO what is XXX supposed to be?
	srv.send_msg(user, "KILL %s :XXX %s" % (user.nick, reason), ctcn.get_hostmask())

	# create a quit event
	modules.quit.handle_event(srv, user, ['[%s] Local kill by %s (%s)' % (srv.name, ctcn.nick, reason)])
