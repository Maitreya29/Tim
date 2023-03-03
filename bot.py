import os
import telebot
from dotenv import load_dotenv
import json
from urllib.request import urlopen, urlretrieve, build_opener, install_opener
from urllib.error import HTTPError
from PIL import Image
import utils

load_dotenv()

API_KEY = os.getenv("API_KEY")
OW_KEY = os.getenv("OW_KEY")
C_KEY = os.getenv("C_KEY")
bot = telebot.TeleBot(API_KEY)
APPROVED_CHATS = os.getenv("APPROVED_CHATS").split(", ")

def isAdmin(id):
	return bot.get_chat_administrators(id)

@bot.my_chat_member_handler()
def my_chat_m(message: telebot.types.ChatMemberUpdated):
	old = message.old_chat_member
	new = message.new_chat_member
	if new.status == "member":
		if(str(message.chat.id) in APPROVED_CHATS):
	        	bot.send_message(message.chat.id, "Hi, I'm a stupid bot.")
		else:
			#bot.send_message(message.chat.id, str(message.chat.id)+str(APPROVED_CHATS))
			bot.send_message(message.chat.id, "I'm not supposed to be in this group.")
			bot.leave_chat(message.chat.id)

@bot.message_handler(commands=["cat"])
def cat(message):
	call="https://api.thecatapi.com/v1/images/search?api_key="+C_KEY
	response = urlopen(call)
	data = json.loads(response.read())
	opener = build_opener()
	opener.addheaders = [('User-Agent', 'TimBot/1.0')]
	install_opener(opener)
	urlretrieve(data[0]["url"], "cat.jpg")
	bot.send_photo(message.chat.id, Image.open("cat.jpg"))
	os.system("rm -rf cat.jpg")

@bot.message_handler(commands=["echo"])
def echo(message):
	content=message.text.replace("/echo", "").strip()
	try:
		bot.send_message(message.chat.id, content)
		bot.delete_message(message.chat.id, message.id)
	except:
		if(content != ""):
			bot.send_message(message.chat.id, "I'm either not admin or the original message was deleted")

@bot.message_handler(commands=["weather"])
def weather(message):
	run = True
	text=message.text
	content=message.text.replace("/weather", "").strip().replace(" ", "%20")
	if(len(content) != 0):
		call="https://api.openweathermap.org/data/2.5/weather?q="+content+"&appid="+OW_KEY
		try:
			response = urlopen(call)
		except HTTPError as err:
			run=False
#		print(response.read())
		if(run == True):
			data = json.loads(response.read())
			temp = "Current Temperature: \n"+ utils.processTemp(data["main"]["temp"])
		else:
			temp = "There was either an error or the location entered by you is invalid/not found."
		bot.reply_to(message, temp)
	else:
		bot.reply_to(message, "Please enter some data")

bot.polling()

