#!/usr/bin/env python3
# encoding=utf8
import flask, config, os, requests, json
from bot import on_msg_receive, time_atual, forward_to_msg, callback_query, service_to_message

app = flask.Flask(__name__)		
from bot import loadplugins

def init():
	#https://api.telegram.org/bot<TOKEN>/setwebhook?url=https://www.example.com/webhook/telegram&max_connections=1&allowed_updates=["message", "edited_message", "callback_query", "inline_query", "chosen_inline_result"]

	try:
		url 	= config.BOT['API'].format(token=config.BOT['token'],method='setWebhook')
		headers = headers={"Content-Type": "application/json"}
		dumps   = ["message",
				   "edited_message",
				   "callback_query",
				   "inline_query",
				   "chosen_inline_result"
				   ]
		params  = {"url": "{}/webhook/telegram".format(config.Sys['host']),
				   "max_connections": 1,
				   "allowed_updates": json.dumps(dumps)}
		data    = requests.get(url, headers=headers, params=params)
		
		print(data)
	
	except Exception as error:
		print(error)

	return 'ok'

def parser_handler(msg):

	message = msg['message']

	if msg.get('callback_query'):
		callback_query(msg['callback_query'])
	
	elif message.get('new_chat_member') or message.get('left_chat_member') or message.get('group_chat_created'):
		service_to_message(msg['message'])
	
	elif msg.get('edited_message'):
		msg['message'] = msg['edited_message']
		msg['edited_message'] = None
	
	elif message.get('forward_from'):
		forward_to_msg(message)
	
	elif message.get('reply_to_message'):
		rethink_reply(message)
	
	else:
		on_msg_receive(message)

@app.before_first_request
def init_():
	from langs import lang
	from bot import sendAdmin
	print("\033[31m  {}\n  {} ".format(lang('int', 'main', sudo='True'), lang('id_text', 'main', sudo='True').format(config.BOT['id'])))
	sendAdmin(text="<b>{}</b>".format(lang('int', 'main', sudo='True')), parse_mode="HTML")

@app.before_request
def handler_():
	
	
	request = flask.request

	if request.method   == 'GET':
		if request.path == "/webhook_int":
			init()
	
	if request.method   == 'POST':
		if request.path == "/webhook/telegram":
			
			msg = request.get_json(silent=True, force=True)
			
			if config.Sys['debug_request'] == True:
				print(json.dumps(msg, indent=1))
			
			if time_atual(msg['message']['date']) > 10:
				return flask.Response(status=200)
			
			if msg.get('message') or msg.get('callback_query') or msg.get('edited_message'):
				parser_handler(msg)

@app.errorhandler(404)
def server_error(e):
	return flask.Response(status=200)

if __name__ == '__main__':
	loadplugins()
	app.run(debug=config.Sys['debug_main'], port=int(os.getenv('PORT', 3000)), host='0.0.0.0')
