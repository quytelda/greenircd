#
# kick.py
# Copyright (C) 2014 Quytelda Gaiwin
#

from channel import IRCChannel

import modules.names

__command__ = "KICK"

# (:prefix) KICK <#target> <user> (:reason)
def handle_event(srv, ctcn, params):
	if len(params) < 2:
		srv.send_msg(user, "461 %s KICK :KICK takes at least 2 parameters!" % user.nick)
		return
	
	target = params[0]
	nick = params[1]
	reason = params[2] if (len(params) > 2) else ctcn.nick
	
	# must be a valid channel
	if not target in srv.channels:
		srv.send_msg(user, "403 %s %s :Channel %s doesn't exist." % (ctcn.nick, target, target))
		return
	channel = srv.channels[target]
	
	# user must be a valid user
	if not nick in srv.clients:
		srv.send_msg(ctcn, "401 %s %s :Nickname not in server database." % (ctcn.nick, nick))
		return
	user = srv.clients[nick]
	
	# user must already be in the channel
	if not user in channel.members:
		srv.send_msg(user, "482 %s %s :User is not in channel." % (ctcn.nick, target))
		return
	user_status = channel.members[user]
	
	# only channel operators can kick
	if (not ctcn in channel.members) or (channel.members[ctcn] < 2**3 and (not user.has_mode('o'))):
		srv.send_msg(user, "482 %s %s :You must be a channel operator to use KICK." % (ctcn.nick, target))
		return

	# can't kick someone with higher access level
	if channel.members[user] >= channel.members[ctcn]: return
	
	# apply the kick
	srv.announce_channel(ctcn, channel, 'KICK %s %s :%s' % (target, nick, reason), ctcn.get_hostmask())
	channel.part(user)
	
	print "*", nick, "was kicked from from", target, "by", ctcn.nick
	
	
