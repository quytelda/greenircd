# numeric.py - numeric replies defined in IRC protocol RFC
#
# Copyright (C) 2014 Quytelda Gaiwin <admin@tamalin.org>
#
# This file is part of GreenIRCd, the python IRC daemon.
#
# GreenIRCd is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GreenIRCd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GreenIRCd.  If not, see <http://www.gnu.org/licenses/>.

RPL_WELCOME = 1
RPL_YOURHOST = 2
RPL_MYINFO = 4
RPL_ISUPPORT = 5
RPL_UMODEIS = 221 # <user_modes> [<user_mode_params>]
RPL_ADMINME = 256 # <server> :<info>
RPL_ADMINEMAIL = 259 # :<email>
RPL_AWAY = 301
RPL_UNAWAY = 305 # :<info>
RPL_NOWAWAY = 306 # :<info>
RPL_WHOISUSER = 311 # <nick> <user> <host> * :<real_name>
RPL_WHOISSERVER = 312 # <nick> <server> :<server_info>
RPL_WHOISOPERATOR = 313 # <nick> :priveleges
RPL_WHOWASUSER = 314
RPL_ENDOFWHO = 315 # <name> :<info>
RPL_ENDOFWHOIS = 318
RPL_WHOISCHANNELS = 319
RPL_LISTSTART = 321 # Channels :Users Name
RPL_LIST = 322 # <channel> <#_visible> :<topic>
RPL_LISTEND = 323 # :info
RPL_CHANNELMODEIS = 324 # <channel> <mode> <mode_params>
RPL_TOPIC = 332 # <channel> :<topic>
RPL_WHOREPLY = 352 # <channel> <user> <host> <server> <nick> <H|G>[*][@|+] :<hopcount> <real_name>
RPL_NAMREPLY = 353 # ( '=' / '*' / '@' ) <channel> ' ' : [ '@' / '+' ] <nick> *( ' ' [ '@' / '+' ] <nick> )
RPL_ENDOFNAMES = 366 # <channel> :<info>
RPL_REHASHING = 382 # <config_file> :<info>
ERR_NOSUCHNICK = 401 # <nick> :<reason>
ERR_NOSUCHCHANNEL = 403 # <channel> :<reason>
ERR_CANNOTSENDTOCHAN = 404 # <channel> :<reason>
ERR_NONICKNAMEGIVEN = 431
ERR_NICKNAMEINUSE = 433 # <nick> :<reason>
ERR_NOTREGISTERED = 451 # :<reason>
ERR_NEEDMOREPARAMS = 461 # <command> :<reason>
ERR_ALREADYREGISTERED = 462 # :<reason>
ERR_CHANNELISFULL = 471 # <channel> :<reason>
ERR_NOPRIVILEGES = 481 # :<reason>
