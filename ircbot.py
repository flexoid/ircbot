#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socket
import string
import time
import threading

class IrcListener(threading.Thread):
	def __init__(self, irc_sock):
		super().__init__()
		self.irc_sock = irc_sock
	
	def run(self):
		while True:
			readbuffer = self.irc_sock.recv(1024)
			temp = str.split(readbuffer.decode("utf8", "ignore"), "\r\n")
			readbuffer = temp.pop()
			
			for line in temp:
				line = str.rstrip(line)
				line = str.split(line)
				
				if(line[0] == "PING"):
					print(str(">> PING {0}").format(line[1]))
					self.irc_sock.send(str("PONG {0}\r\n").format(line[1]).encode("utf8"))
					print(str("<< PONG {0}").format(line[1]))

HOST = "172.31.0.100"
PORT = 6667
NICK = "FlexoBot"
IDENT = "flexobot"
REALNAME = "FlexoBot"
CHANNEL = "#linux"
QUITMESSAGE = "FlexoBot ***python3***"

s = socket.socket()
s.connect((HOST, PORT))

ircListener = IrcListener(s)
ircListener.daemon = True
ircListener.start();

s.send(str("NICK {0}\r\n").format(NICK).encode("utf8"))
s.send(str("USER {0} {1} {1} :{2}\r\n").format(IDENT, HOST, REALNAME).encode("utf8"))
s.send(str("JOIN {0}\r\n").format(CHANNEL).encode("utf8"))

while True:
	msg = input(str("Message to {0}: ").format(CHANNEL))
	if msg == "!quit":
		break
	if msg != "":
		s.send(str("PRIVMSG {0} :{1}\r\n").format(CHANNEL, msg).encode("utf8"))

s.send(str("QUIT {0}\r\n").format(QUITMESSAGE).encode("utf8"))
