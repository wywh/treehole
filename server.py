# -*- coding: utf-8 -*-
#
#This source code was published under GPL v3
#
#Copyright (C) 2017 Too-Naive
#
import telepot
import time
from config import botToken,sqlhost,sqlport,sqluser,sqlpwd,sqlname
import sys
from mysqlmodule import mysqlModule as mm

bot = None


def onMessage(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(content_type, chat_type, chat_id)
	if chat_type != 'private' or content_type!= 'text':
		return
	sql = mm(sqlhost,sqlport,sqluser,sqlpwd,sqlname)
	pass

def main():
	global bot
	bot = telepot.Bot(botToken)
	bot.message_loop(onMessage)
	while True:
		time.sleep(10)

def init():
	reload(sys)
	sys.setdefaultencoding('utf8')

if __name__ == '__main__':
	init()
	main()
