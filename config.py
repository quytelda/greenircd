#
# config.py - GreenIRCd configuration functions
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
# WeeChat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GreenIRCd.  If not, see <http://www.gnu.org/licenses/>.

import ConfigParser

def config(srv, path, init = True):
	parser = ConfigParser.ConfigParser()
	parser.read(path)
	
	srv.config = path
	srv.opers = []

	for section in parser.sections():
		if section.startswith('server:'):
			# get name
			if init:
				srv.name = section.replace('server:', '')
			
			# get port listening configuration
			if ('ports-client' in parser.options(section)) and init:
				port_list = parser.get(section, 'ports-client')
				ports = [int(p) for p in port_list.replace(' ', '').split(',')]
				if len(ports) > 0: srv.ports_client = ports
			if ('ports-client-ssl' in parser.options(section)) and init:
				port_list = parser.get(section, 'ports-client-ssl')
				ports = [int(p) for p in port_list.replace(' ', '').split(',')]
				if len(ports) > 0: srv.ports_client_ssl = ports
			if ('ports-server' in parser.options(section)) and init:
				port_list = parser.get(section, 'ports-server')
				ports = [int(p) for p in port_list.replace(' ', '').split(',')]
				if len(ports) > 0: srv.ports_server = ports
			if ('ports-server-ssl' in parser.options(section)) and init:
				port_list = parser.get(section, 'ports-server-ssl')
				ports = [int(p) for p in port_list.replace(' ', '').split(',')]
				if len(ports) > 0: srv.ports_server_ssl = ports
				
			# get info
			if 'info' in parser.options(section):
				srv.info = parser.get(section, 'info')
				
			# autojoin
			if 'autojoin' in parser.options(section):
				srv.autojoin = parser.get(section, 'autojoin')
				
			if 'operjoin' in parser.options(section):
				srv.operjoin = parser.get(section, 'operjoin')
				
			if 'connect-modes' in parser.options(section):
				srv.connect_modes = parser.get(section, 'connect-modes')
				
		if section.startswith('oper:'):
			oper = {}
		
			# get login
			oper['username'] = section.replace('oper:', '')
			
			# get auth
			oper['auth'] = parser.get(section, 'auth')
			
			# get flags
			if 'flags' in parser.options(section):
				oper['flags'] = parser.get(section, 'flags')
			else:
				oper['flags'] = 'o'
				
			srv.opers.append(oper)
		
		if section.startswith('link:'):
			link = {}
			name = section.replace('link:', '')
			
			# get auth
			link['lauth'] = parser.get(section, 'local-auth')
			link['rauth'] = parser.get(section, 'remote-auth')
			link['host'] = parser.get(section, 'host')
				
			srv.links[name] = link
