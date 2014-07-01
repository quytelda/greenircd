#
# wallops.py
#

import symbols

__command__ = 'WALLOPS'

def handle_event(srv, ctcn, params):
	
	# only opers can send wallops
	if not ctcn.has_mode('o'): return

	msg = ' '.join(params)
	print "* WALLOPS:", msg
	for nick in srv.clients:
		user = srv.clients[nick]
		if user.has_mode('w'):
			srv.send_msg(user, 'WALLOPS :%s' % (msg), ctcn.get_hostmask())
