import os
import telebot
import requests
from flask import Flask, request

TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'Отправь мне голосовое сообщение, а я верну аудиофайл, чтобы ты смог его сохранить')

@bot.message_handler(content_types=['voice'])
def echo_all(message):
	voice_id = message.voice.file_id
	file_info = bot.get_file(message.voice.file_id)
	file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(f'{TOKEN}', file_info.file_path))
	open(f'{voice_id}.oga', 'wb').write(file.content)
	os.rename(rf'{voice_id}.oga',rf'{voice_id}.mp3')
	doc = open(f'{voice_id}.mp3', 'rb')
	bot.send_audio(message.chat.id, doc)
	doc.close()
	os.remove(f'{voice_id}.mp3')

@server.route('/', methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200

if __name__ == "__main__":
	server.run()