import telebot
from requests_html import HTMLSession

bot = telebot.TeleBot("1940148984:AAELX6QJlYiSplwpmb4_dzsvGz04ryZUjDA")

@bot.message_handler(commands=['start','help'])
def weather(message):
    text = "Hello! This Bot is still in Beta! Current available commands are: /weather, /car"
    bot.reply_to(message, text)

@bot.message_handler(commands=['weather'])
def weather(message):
    session = HTMLSession()
    r = session.get('https://www.hko.gov.hk/textonly/v2/forecast/chinesewx2.htm')
    weather = r.html.xpath('//*[@id="ming"]/text()', first=True)
    bot.reply_to(message, weather)

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

bot.polling()