#
# nick.py
#

__command__ = 'NICK'

# NICK <nickname> [<hopcount>]
def handle_event(srv, ctcn, params):
	if len(params) < 1:
		srv.send_msg(ctcn, "431 %s %s :The NICK command requires one parameter!")
		return
	target = params[0]
	
	# can't use a nick that's already in use
	if (target in srv.clients):
		srv.send_msg(ctcn, "433 %s %s :The nickname %s is already in use." % (ctcn.nick, target, target))
		return
	
	# we might be changing nicks from an existing one
	old_nick = ctcn.nick if hasattr(ctcn, 'nick') else None
	
	# apply the nick change to ourselves
	setattr(ctcn, 'nick', target)
	
	# if the user exists on the server already with a nick
	if old_nick in srv.clients:
		# announce the nick change
		srv.clients[target] = srv.clients.pop(old_nick)
		srv.announce(ctcn, 'NICK %s' % (target), old_nick, False)
	# if the user has just completed registration
	elif hasattr(ctcn, 'uid'): # all info necessary to register is present
		srv.register_client(ctcn)
