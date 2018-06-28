#!/usr/bin/python
#-*- coding: utf-8 -*-
from TelegramBOT import sendAdmin, config, plugins_, bash_, json
def Function(msg, cmd, ln):
	global maintenance
	if 'sudo' in cmd[0]:
			if (cmd[1] == 'att'):
				sendAdmin(chat_id=msg['chat']['id'], text="Done")
				return plugins_()

			elif (cmd[1] == 'manut'):
				config['MAINTENACE'] = True
				sendAdmin(chat_id=msg['chat']['id'], text="Done")
				return config['MAINTENACE']

			elif (cmd[1] == 'notmanut'):
				config['MAINTENACE'] = False
				sendAdmin(chat_id=msg['chat']['id'], text="Done")
				return config['MAINTENACE']
	elif ('shell' in cmd[0]) or ('git' in cmd[0]):
		sendAdmin(chat_id=msg['chat']['id'],text=bash_(cmd[0], cmd[1]))
	elif 'debug' in cmd[0]:
				if len(cmd) ==2 and cmd[1] == "user" and "reply" in msg:
					sendAdmin(chat_id=msg['chat']['id'],text="<code>{}</code>".format(json.dumps(msg['reply']['from'], indent=1)), parse_mode="HTML")
				else:
					sendAdmin(chat_id=msg['chat']['id'],text="<code>{}</code>".format(json.dumps(msg, indent=1)), parse_mode="HTML")
	
plugin = {
	'patterns': [
		"^[/!#](sudo) (att)$",
		"^[/!#](sudo) (manut)$",
		"^[/!#](sudo) (notmanut)$",
		"^[/!#](shell) (.+)$",
		"^[/!#](git) (.+)$",
		"^[/!#](debug)$",
		"^[/!#](debug) (user)$"
	],
	'function': Function,
	'name': "Admin",
	'sudo': True,
	}