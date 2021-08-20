import os
from dotenv import load_dotenv
import telebot
from requests_html import HTMLSession

#Setup Bot Token
load_dotenv()
API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start','help'])
def start(message):
    text = "Hello! This Bot is still in Beta! Current available commands are: /weather, /car. There has a hidden function to my gf to calulate the time."
    bot.reply_to(message, text)

@bot.message_handler(commands=['weather'])
def weather(message):
    session = HTMLSession()
    r = session.get('https://www.hko.gov.hk/textonly/v2/forecast/chinesewx2.htm')
    weather = r.html.xpath("//pre[@id='ming']/text()")
    try:
        p = r.html.xpath("//pre[@id='ming']/p/text()", first=True)
    except ValueError:
        pass
    if " " in p:
        bot.reply_to(message, weather[0]+p+"\n"+weather[1])
    else:
        bot.reply_to(message, weather[0]+weather[1])

import datetime as dt
@bot.message_handler(commands=['car'])
def weather(message):
    session = HTMLSession()
    today = dt.date.today()
    today = (str(today).split('-'))
    web = "https://programme.rthk.hk/channel/radio/trafficnews/index.php?d={}{}{}".format(today[0],today[1],today[2])
    r = session.get(web)
    article = r.html.xpath('//*[@id="content"]/div/ul')
    article_rev = []
    carInfo = ""
    if article == []:
        carInfo = "Currently no news."
    else:
        for news in article:
            article_rev.insert(0,news)

        for info in article_rev[-10:]:
            carInfo += info.text+"\n\n"
    bot.reply_to(message, carInfo)

@bot.message_handler(func=lambda message: message.text is not None and len(message.text) == 11 and ':' in message.text and '-' in message.text)
def cal_time(message):
    try:
        start_time, end_time = message.text.split('-')
        s_h, s_m= start_time.split(':')
        e_h, e_m= end_time.split(':')
        start_time = dt.datetime.strptime(start_time,'%H:%M')
        end_time = dt.datetime.strptime(end_time,'%H:%M')
        result = end_time - start_time
        bot.reply_to(message, result)
    except ValueError:
        result = "It seems not a correct format."
        bot.reply_to(message, result)

bot.polling()