#
# kick.py
# Copyright (C) 2014 Quytelda Gaiwin
#

from channel import IRCChannel

import modules.names

__command__ = "KICK"

# (:prefix) KICK <#target> <user> (:reason)
def handle_event(srv, ctcn, params):
	if len(params) < 2: return
	
	target = params[0]
	nick = params[1]
	reason = ' '.join(params[2:]) if (len(params) > 2) else ctcn.nick
	
	# must be a valid channel
	if not target in srv.channels: return
	channel = srv.channels[target]
	
	# user must be a valid user
	if not nick in srv.clients: return
	user = srv.clients[nick]
	
	# user must already be in the channel
	if not user in channel.members: return
	user_status = channel.members[user]
	
	# only channel operators can kick
	if (not ctcn in channel.members) or (channel.members[ctcn] < 2**3 and (not user.has_mode('o'))): return
	
	# can't kick someone with higher access level
	if channel.members[user] > channel.members[ctcn]: return
	
	# apply the kick
	srv.announce_channel(ctcn, channel, 'KICK %s %s :%s' % (target, nick, reason), ctcn.get_hostmask())
	channel.part(user)
	
	print "*", nick, "was kicked from from", target, "by", ctcn.nick
	
	
