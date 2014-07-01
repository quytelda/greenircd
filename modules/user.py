#
# user.py
#

__command__ = 'USER'

def handle_event(srv, ctcn, params):
	uid = params[0]

	if (not ctcn in srv.clients) and (not hasattr(ctcn, 'uid')): # not yet registered with the server
		setattr(ctcn, 'uid', uid)
		if hasattr(ctcn, 'nick'): # all info necessary to register is present
			srv.register_client(ctcn)
