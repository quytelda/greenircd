#
# kill.py
# Copyright (C) Quytelda Gaiwin
#

import symbols

__command__ = 'KILL'

def handle_event(srv, ctcn, params):
	print "* KILL command used!"

	if len(params) < 1: return
	
	# only operators can use KILL
	if not ctcn.has_mode('o'): return
	
	print "* received KILL"
	
	target = params[0]
	reason = ' '.join(params[1:]) if (len(params) > 1) else 'Killed'
	
	# if the target doesn't exist, send a 401 and exit
	if not target in srv.clients:
		srv.send_msg(ctcn, "401 %s :%s is not a known nick or channel!" % (target, target))
		return
	
	print "* executing KILL command on", target
	
	# send the kill notice
	srv.announce(ctcn, "KILL %s :%s" % (target, reason), ctcn.get_hostmask())
	
	# apply the action
	client = srv.clients[target]
	client.loseConnection()
	#srv.unregister_connection(client)
