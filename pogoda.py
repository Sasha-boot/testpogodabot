# ПРОГНОЗ ПОГДЫ v2
import pyowm
import telebot

owm = pyowm.OWM('bc48aa759c9c8cc16f9a2ac2164aad2c', language="ru")
bot = telebot.TeleBot("1119552349:AAEqwr_F3TV76UXuxp3IYiXml_0O_FtdmGo")

@bot.massage_handler(commands=['start'])
def welcome(message):
    sti = open('static/sticker.webp', "rb")
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, тестовый погода бот !".format(message.from_user, bot.get_me()),
        parse_mode='html')

@bot.message_handler(content_types=["text"])
def send_echo(message):
    observation = owm.weather_at_place(message.text)
    w = observation.get_weather()
    detail = w.get_detailed_status()
    temp = w.get_temperature('celsius')["temp"]
    hum = w.get_humidity()
    speed = w.get_wind()["speed"]

    answer = "В городе "+message.text+" сейчас "+str(detail)+" \nТемпература: "+str(temp)+" °С \nВлажность: "+str(hum)+" % \nСкорость ветра: "+str(speed)+" м/с"

# Рекомендации
    if temp < 5:
	    answer += "\n\nНа улице очень холодно , 'в халупе сиди, листком подтирайся :D' "
    elif temp > 20:
	    answer += "\n\nНА УЛИЦЕ ЖАРА! ГУЛЯЕМ МАЛЬЧИКИ , ВЕСНА !"
    elif temp > 5:
	    answer += "\n\nНа рассвете тёплый восточный ветер пригонит к нам тёплое солнышко, которое пролетит над всем городом и вечером улетит на запад…"
    elif temp > 30: 
	    answer += "\n\nсолнышко рядом"
    else:
	    print("\n\nМогу поздравть тебя ! ты не умеешь писать !")

    bot.send_message(message.chat.id, answer)

bot.polling(none_stop=True)
