# ПРОГНОЗ ПОГДЫ v3
import pyowm
import telebot

bot = telebot.TeleBot("1119552349:AAEqwr_F3TV76UXuxp3IYiXml_0O_FtdmGo")
owm = pyowm.OWM('bc48aa759c9c8cc16f9a2ac2164aad2c', language ="ru")


@bot.message_handler(commands=['start'])
def start_message(message):
    sti = open('stabc/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "Приветствую тебя {0.first_name}!\nЯ - <b>{1.first_name}</b>, погода бот !\n\nЧтобы узнать погоду в твоем городе\nПросто пиши его название\nПример - 'Москва' ".format(message.from_user, bot.get_me()),
        parse_mode='html')


@bot.message_handler(content_types=["sticker", "pinned_message", "photo", "audio"])
def send_message(message):
   
    reply = "Класс"  

    bot.send_message(message.chat.id, reply)	


@bot.message_handler(content_types=["text"])
def send_echo(message):
    try:
        observation = owm.weather_at_place(message.text)    
        w = observation.get_weather()
        temp = w.get_temperature('celsius')["temp"]
        hum = w.get_humidity()
        wind = w.get_wind()["speed"]
        time = w.get_reference_time(timeformat='iso')        

        answer ="В городе " + message.text + " сейчас " + w.get_detailed_status() + "\n"
        answer += "Температура в районе " + str(temp) + "\n\n" + "\nСкорость ветра: " + str(wind) + "м/с" + "\n" + "\nВлажность: " + str(hum) + "%" + "\n" + "\nВремя: " + str(time) + "\n"       

        if temp < 0:
            answer +="На улице очень холодно! Сиди лучше дома."
        elif temp > 5:
            answer +="На улице прохладно. Оденься по теплее и вперед !!"
        elif temp > 15:
            answer +="На улице тепло, одевай кофту и гуляй !!!"
        elif temp > 20:
            answer +="НА УЛИЦЕ ЖАРА ! ГУЛЯЕМ МАЛЬЧИКИ ВЕСНА !!!! "

            	
        bot.send_message(message.chat.id, answer)
    except:
        bot.send_message(message.chat.id, "ПОШЕЛ НА ХУЙ !! ")

    	
bot.polling(none_stop=True)
