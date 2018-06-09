from bot import sendMessage, lang
def echo(msg, cmd, ln):
	if len(cmd) >1:
		text    = msg['text'].replace(cmd[0],'')
		if ('<' in text and '>' in text):
			parser = 'HTML'
		elif ('*' in text or '_' in text or '`' in text or '[' in text and '(' in text):
			parser = 'Markdown'
		else:
			parser = ''
		try   :sendMessage(chat_id=msg['chat']['id'], text=text, parse_mode=parser, reply_to_message_id=msg['message_id'])
		except:sendMessage(chat_id=msg['chat']['id'], text=lang('echo', ln)[0]['parser_error'], parse_mode=parser, reply_to_message_id=msg['message_id'])
	else:
		return lang('echo', ln)[0]['help']
plugin = {
	'patterns': [
		"^/(echo)",
		"^/(repita)",
		
	],
	'function': echo,
	'name': "Echo",
	'sudo': False,
	}