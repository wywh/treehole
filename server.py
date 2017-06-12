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
import datetime
import re

bot = None

def datetimeFromNow(timestamp):
	return datetimeFromNowEx(datetime.datetime.now(),timestamp)

def datetimeFromNowEx(timestampnow,timestamp):
	return (timestampnow.replace(microsecond=0)-timestamp).total_seconds()

def sendMessage2Group(chatGroup):
	global bot
	for x in chatGroup:
		bot.sendMessage(chatGroup)

def onMessage(msg):
	global bot

	MESSAGE_PEAR_DAY = 3
	MESSAGE_PEAR_CYCLE = 60*60*24
	MESSAGE_COLD_DOWN_CYCLE = 60*5

	content_type, chat_type, chat_id = telepot.glance(msg)
	if chat_type != 'private' or content_type!= 'text':
		return
	nowtimestamp = datetime.datetime.now()
	sql = mm(sqlhost,sqlport,sqluser,sqlpwd,sqlname)
	result = mm.query("SELECT * FROM `users` WHERE `user_id` = %d"%chat_id)
	if not result and msg['text'] == '/ACCEPT':
		sql.execute("INSERT INTO `users` (`user_id`) VALUES (%d)"%chat_id)
		sql.close()
		return
	if not result:
		bot.sendMessage(chat_id,"PLEASE SEND /ACCEPT TO ACCEPT OUR LICENSES AGREEMENT")
		sql.close()
		return
	if result[0][2] == 1:
		bot.sendMessage(chat_id,"YOU HAS BEEN BLOCKED, PLEASE CONTACT ADMINISTRATOR")
		sql.close()
		return
	elif datetimeFromNow(result[0][5]) > MESSAGE_COLD_DOWN_CYCLE5:
		if datetimeFromNow(result[0][4]) > MESSAGE_PEAR_CYCLE:
			sql.execute("UPDATE `users` SET `messageCycleTS` = TIMESTAMP(), `messagesInCycle` = 1 WHERE `user_id` = %d"%chat_id)
		elif result[0][6] < MESSAGE_PEAR_DAY:
			sql.execute("UPDATE `users` SET `messagesInCycle` = %d WHERE `user_id` = %d"%(result[0][6],chat_id))
		else:
			sql.close()
			return
		result = sql.query("SELECT `user_id` FROM `users` WHERE `isForwardTarget` = 1")
		sendMessage2Group((x[0] for x in result))
		sql.close()
		pass
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
