import os
import telebot
from dotenv import load_dotenv
import json
from urllib.request import urlopen
from urllib.error import HTTPError

load_dotenv()

API_KEY = os.getenv("API_KEY")
OW_KEY = os.getenv("OW_KEY")
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=["weather"])
def greet(message):
	run = True
	text=message.text
	content=message.text.replace("/weather", "").strip()
	if(len(content) != 0):
		call="https://api.openweathermap.org/data/2.5/weather?q="+content+"&appid="+OW_KEY
		try:
			response = urlopen(call)
		except HTTPError as err:
			run=False
#		print(response.read())
		if(run == True):
			data = json.loads(response.read())
			temp = "Current Temperature: \n"+ processTemp(data["main"]["temp"])
		else:
			temp = "There was either an error or the location entered by you is invalid/not found."
		bot.reply_to(message, temp)
	else:
		bot.reply_to(message, "Please enter some data")
def processTemp(kelvin):
	celsius = kelvin-273.15
	farenheit = (celsius * 9/5)+32
	return str(round(celsius, 2))+"°C | "+str(round(farenheit, 2))+"°F | "+str(round(kelvin,2))+"K"

bot.polling()

