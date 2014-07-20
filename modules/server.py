# server.py
#
# Copyright (C) 2014 Quytelda Gaiwin

import irc.server

__command__ = 'SERVER'
preregister = True

# SERVER Syntax: :prefix SERVER <servername> <hopcount> :<info>
def handle_event(srv, source, params):
	# SERVER messages from clients will be ignored
	# same for already registered servers
	if (source in srv.clients.values()) or (source in srv.servers.values()): return
	
	# SERVER messages must be delivered over a server connection port
	if not source.ctcn.transport.getHost().port in srv.ports_server:
		print "* SERVER message from client port dropped!"
		return
	
	# must have three parameters
	if len(params) < 3:
		return
		
	servername = params[0]
	hops = params[1]
	info = params[2]
	
	# check if there is a matching link entry
	if not servername in srv.links:
		print "* Unidentified SERVER message dropped!"
		return
	
	# the IP from that entry must match
	if not srv.links[servername]['host'] == source.ctcn.host['ip']:
		print "* SERVER message from unapproved source dropped!"
		return 
	
	# the link is new initiated, so respond with the appropriate message
	print "*", servername, "initiating link..."
	
	# register the link with the server
	# we can now upgrade the connection to a server container
	server = irc.server.IRCServer(source.ctcn, servername, hops, info)
	srv.servers[servername] = server
	source.ctcn.message("SERVER %s 0 :%s" % (srv.name, srv.info))
	print "!!!srv.servers", srv.servers
