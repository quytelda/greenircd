#
# kill.py
# Copyright (C) Quytelda Gaiwin
#

import symbols

__command__ = 'KILL'

def handle_event(srv, ctcn, params):
	if len(params) < 1:
		srv.send_msg(ctcn, "461 %s KILL :KILL takes at least 1 parameter!" % ctcn.nick)
		return
	
	# only operators can use KILL
	if not ctcn.has_mode('o'):
		srv.send_msg(ctcn, "481 %s :You must be an operator to use KILL." % ctcn.nick) 
		return
	
	target = params[0]
	reason = params[1] if (len(params) > 1) else ctcn.nick
	
	# if the target doesn't exist, send a 401 and exit
	if not target in srv.clients:
		srv.send_msg(ctcn, "401 %s :Nickname not in server database." % ctcn.nick)
		return
	
	user = srv.clients[target]
	
	# announce the kill notice
	# TODO what is 'xxx' supposed to be?
	srv.announce_common(ctcn, "KILL %s :xxx %s" % (user.nick, reason), ctcn.get_hostmask())

	# apply the action
	user.close()
