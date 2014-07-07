# server.py
#
# Copyright (C) 2014 Quytelda Gaiwin

__command__ = 'SERVER'

# SERVER Syntax: :prefix SERVER <servername> <hopcount> :<info>
def handle_event(srv, ctcn, params):
	# SERVER messages from clients will be ignored
	if ctcn in srv.clients: return
	
	# must have three parameters
	if len(params) < 3:
		return
		
	servername = params[0]
	hops = params[1]
	info = params[2]
	
	#TODO validate the info
	
	
	setattr(ctcn, 'name', servername)
	setattr(ctcn, 'hops', hops)
	setattr(ctcn, 'info', info)
	
	srv.servers[servername] = ctcn
