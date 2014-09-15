GreenIRCD is a simple IRC daemon written in Python. GreenIRCD aims to be simple and easy to configure and use.

Features:

    Extended channel status modes (+qaohv)
    Hostname cloaking
    vHosts
    SSL encrypted connections
    Configurable Opers/Admins
    Pluggable modules
    UTF-8 Support

Planned Features (on the agenda):

    Server Linking (GreenIRCd)
    Connection Throttling
    Linked or Integrated Services
    (Extended) Server and Channel Bans


Supports the following commands:
JOIN, PART, QUIT, NICK, USER, LIST, WHO, WHOIS, MODE, PRIVMSG, NOTICE, NAMES, TOPIC, KICK, KILL, OPER, WALLOPS

Supports the following modes:
Channel Modes: OPahmlonqstv
	MODE	MEANING
	O		oper only channel
	P		never opless channel (persist ops)
	a*		gives admin (&)
	h*		gives halfop (%)
	m		moderated
	l*		limit
	o*		gives chanop (@)
	n		no outside messages
	q*		gives owner (~)
	s		secret
	t		restrict topic changes
	v		gives voice (+)
* takes a parameter

User Modes: aqowxi
	MODE	MEANING
	a		administrator
	q		protected
	o		server operator
	w		receives wallops
	x		cloaked host
	i		invisible		
