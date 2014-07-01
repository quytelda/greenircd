#
# names.py
#

__command__ = "NAMES"

def handle_event(srv, ctcn, params):
	channel = params[0]
	
	nam_list = srv.channels[channel].names()
	
	srv.send_msg(ctcn, '353 %s = %s :%s' % (ctcn.nick, channel, nam_list))
	srv.send_msg(ctcn, '366 %s %s :%s' % (ctcn.nick, channel, "End of /NAMES List"))
