# This program is a chatbot that uses PyAIML and xmpppy
#
# Original Author - Harshad Joshi
# Modified By - [Your Name]
#
# Date - May 6, 2011 / May 11, 2015
# Last Modified - [Current Date]
#
# Requirements - XMPP chat server (openfire)
#              - Python 3.x with xmpp and PyAIML library.
#
# Features - Unicode enabled
#
# ToDo - Bot gets kicked off after being idle for 5 or 6 minutes. Needs to send 'KeepAlive' packet.
#      - After getting logged in, it posts 'None' as the first message. Need to remove it.
#      - Doesn't work with gtalk. I don't know the reason.
#      - Should ask for the user's details once and store them in the backend.


import sys
import time
import datetime
import xmpp
import codecs
import aiml
import mysql.connector


# User details
user = 'jabber_account@server.com'
password = 'your_password'
server = 'jabber_server.com'


# Initialize the AIML kernel and load the AIML files
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")


# Initialize the MySQL database
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='chat_logs'
)


# Create a table to store chat logs
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS logs (id INT AUTO_INCREMENT PRIMARY KEY, date_time DATETIME, sender TEXT, message TEXT)")


# Handle presence and subscription - automatically subscribe to user who requests subscription (not recommended for public use)
def presence_handler(connection_object, message_node):
    prs_type = message_node.getType()
    who = message_node.getFrom()

    if prs_type == "subscribe":
        connection_object.send(xmpp.Presence(to=who, typ='subscribed'))
        connection_object.send(xmpp.Presence(to=who, typ='subscribe'))


# Handle incoming messages
class Bot:
    def message_handler(connect_object, message_node):
        command = str(unicode(message_node.getBody()).encode('utf-8'))
        sender = str(message_node.getFrom().getStripped())
        response = kernel.respond(command)

        # Store chat log in MySQL database
        cursor = db.cursor()
        cursor.execute("INSERT INTO logs (date_time, sender, message) VALUES (%s, %s, %s)", (datetime.datetime.now(), sender, response))
        db.commit()

        # Send the response to the user
        connect_object.send(xmpp.Message(sender, response))

    jid = xmpp.JID(user)
    connection = xmpp.Client(server)
    connection.connect()
    result = connection.auth(jid.getNode(), password)
    connection.RegisterHandler('message', message_handler, "")
    connection.RegisterHandler('presence', presence_handler, "")
    connection.sendInitPresence()

    # Send initial message to indicate that the bot is ready to chat
    press = xmpp.Presence()
    press.setStatus("Hi from the bot! I'm here to chat with you and tell you new things you might like.")
    connection.send(press)

    while True:
        connection.Process(1)


if __name__ == '__main__':
    Bot()    
