#
# nick.py
#

__command__ = 'NICK'

def handle_event(srv, ctcn, params):
	if len(params) < 1: return
	target = params[0]
	
	# can't use a nick that's already in use
	if (target in srv.clients):
		srv.send_msg(ctcn, "433 %s %s :The nickname %s is already in use." % (ctcn.nick, target, ctcn.nick))
		return
	
	old_nick = ctcn.nick if hasattr(ctcn, 'nick') else None
	
	# apply the nick change to ourselves
	setattr(ctcn, 'nick', target)
	
	# if the user exists on the server already with a nick
	if old_nick in srv.clients:
		print "* changing nick from", old_nick, "to", target
		# announce the nick change
		srv.clients[target] = srv.clients.pop(old_nick)
		
		srv.announce(ctcn, 'NICK :%s' % (target), old_nick, False)
	else:
		if hasattr(ctcn, 'uid'): # all info necessary to register is present
			srv.register_client(ctcn)
		else: # not ready yet, just move on
			print "* unregistered client did nick change"
			return
