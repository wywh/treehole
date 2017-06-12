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
	return (timestampnow.replace(microsecond=0)-timestamp.replace(microsecond=0)).total_seconds()

def sendMessage2Group(chatGroup,msg):
	global bot
	for x in chatGroup:
		bot.sendMessage(x,msg)
		time.sleep(1)

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
	result = sql.query("SELECT * FROM `users` WHERE `user_id` = %d"%chat_id)
	if not result and msg['text'] == '/ACCEPT':
		sql.execute('''
			INSERT INTO `users` 
			(`user_id`,`messageCycleTS`,`lastMessage`) 
			VALUES 
			(
				'''+str(chat_id)+''',
				TIMESTAMP(STR_TO_DATE('1973-01-01 05:00:00','%Y-%m-%d %H:%i:%s')),
				TIMESTAMP(STR_TO_DATE('1973-01-01 05:00:00','%Y-%m-%d %H:%i:%s'))
			)
			''')
		sql.close()
		bot.sendMessage(chat_id,'Congratulations! You can use this bot now.')
		return
	if not result and (msg['text'] == '/license' or msg['text'] == '/start'):
		bot.sendMessage(chat_id,'We guarantee that we will send a message in a completely anonymous way.The bot will only record your '+
			'id and prevent spam from being sent. All messages you send to the bot are '
			'not guaranteed to be published, and we will review your post anonymously.'+
			'Bot code in github : https://github.com/Too-Naive/treehole'+
			'Author : @stdssr')
		return
	if not result:
		bot.sendMessage(chat_id,"PLEASE SEND /ACCEPT TO ACCEPT OUR LICENSES AGREEMENT /license")
		sql.close()
		return
	if result[0][2] == 1:
		bot.sendMessage(chat_id,"YOU HAS BEEN BLOCKED, PLEASE CONTACT ADMINISTRATOR")
		sql.close()
		return
	elif datetimeFromNow(result[0][5]) > MESSAGE_COLD_DOWN_CYCLE:
		if datetimeFromNow(result[0][4]) > MESSAGE_PEAR_CYCLE:
			sql.execute("UPDATE `users` SET `messageCycleTS` = CURRENT_TIMESTAMP, `messagesInCycle` = 1, `lastMessage` = CURRENT_TIMESTAMP WHERE `user_id` = %d"%chat_id)
		if result[0][6] < MESSAGE_PEAR_DAY:
			sql.execute("UPDATE `users` SET `messagesInCycle` = %d, `lastMessage` = CURRENT_TIMESTAMP WHERE `user_id` = %d"%(result[0][6]+1,chat_id))
		else:
			if result[0][6] >= MESSAGE_PEAR_DAY:
				bot.sendMessage(chat_id,'Portal burn out! It may take significant time for the Portal to reset.')
			sql.close()
			return
		result = sql.query("SELECT `user_id` FROM `users` WHERE `isForwardTarget` = 1")
		sendMessage2Group(list(x[0] for x in result),msg['text'])
		bot.sendMessage(chat_id,'Send successfully, Please waiting for review')
		sql.close()
	else: 
		bot.sendMessage(chat_id,'Portal running hot! Unsafe to send messages. Estimated time to cooldown: %d seconds'%calctime(result[0][5],nowtimestamp))
		sql.close()


sec = [5,10,20,30,60,120,180,240,300]


def calctime(timestamp,nowatime):
	global sec
	dec = 300-datetimeFromNowEx(nowatime,timestamp)
	for x in sec:
		if dec <= x:
			return x

def main():
	global bot
	bot = telepot.Bot(botToken)
	bot.message_loop(onMessage)
	while True:
		bot.getMe()
		time.sleep(10)

def init():
	reload(sys)
	sys.setdefaultencoding('utf8')

if __name__ == '__main__':
	init()
	main()
