# This programs is basically a chatbot
# Uses PyAIML and xmpppy
#
# Author       - Harshad Joshi
# Date         - May 6, 2011
#
# Requirements - XMPP chat server (openfire)
#              - Python 2.5 with xmpp and PyAIML library.
#
# Features     - Unicode enabled
#
# ToDo         - Bot gets kicked off after being idle for 5 or 6 minutes. 
#              - Needs to send 'KeepALive' packet.
#              - After getting logged in, it posts 'None' as the first message. Need to remove it.
#	       - Dosent work with gtalk. i dont know the reason.
#              - should ask for it once and store it in the backend.



import sys

import time
import datetime
import xmpp
import codecs
import aiml


user='user@gmail.com'
passwd='gmailpasswd'
server='gmail.com'


# the heart and brain of bot...

k = aiml.Kernel()

k.learn("std-startup.xml")

k.respond("load aiml b")


#this snippet handles presence and subscription...automatically subscribes to user who request subscription. Not recommended for public use.
def presence_handler(connection_object, message_node):
		prstype=message_node.getType()
		who=message_node.getFrom()
		if prstype == "subscribe":
			connection_object.send (xmpp.Presence(to=who,typ = 'subscribed'))
			connection_object.send (xmpp.Presence(to=who,typ = 'subscribe'))


class Bot:
	def message_handler(connect_object,message_node):
		command1=str(unicode(message_node.getBody()).encode('utf-8'))
		command2=str(message_node.getFrom().getStripped())
				
		#the fun begins from this place..
		connect_object.send(xmpp.Message(command2,(k.respond(command1))))				
	
		
	jid=xmpp.JID(user)
	connection=xmpp.Client(server)
	connection.connect()
	result=connection.auth(jid.getNode(),passwd)
	connection.RegisterHandler('message',message_handler,"")
	connection.RegisterHandler('presence',presence_handler,"")	
	connection.sendInitPresence()
        press = xmpp.Presence()
        press.setStatus("Hi from bot...i will chat with you and tell you new things you might like")
        connection.send(press)

	while (1):
		connection.Process(1)

a=Bot()
a

	



