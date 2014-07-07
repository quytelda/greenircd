#
# user.py
#

__command__ = 'USER'
req_register = False

# USER <username> <hostname> <servername> :<realname>
def handle_event(srv, ctcn, params):
	if len(params) < 4:
		srv.send_msg(ctcn, "461 %s USER :USER takes 4 parameters!" % (ctcn.nick if hasattr(ctcn, 'nick') else ''))
		return

	# users can only register once
	if ctcn.nick in srv.clients:
		srv.send_msg(ctcn, "462 %s :You are already registered!" % ctcn.nick)

	username = params[0]
	hostname = params[1]
	server = params[2]
	realname = params[3]

	if (not ctcn in srv.clients) and (not hasattr(ctcn, 'uid')): # not yet registered with the server
		setattr(ctcn, 'uid', username)
		if hasattr(ctcn, 'nick'): # all info necessary to register is present
			srv.register_client(ctcn)
