#
# wallops.py
#

import symbols

__command__ = 'WALLOPS'

def handle_event(srv, source, params):
	# only opers can send wallops
	if not source.has_mode('o'): return

	msg = ' '.join(params)
	for client in srv.clients.values():
		if client.has_mode('w'):
			client.ctcn.message('WALLOPS :%s' % msg, source.hostmask())
