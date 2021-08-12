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

bot.polling()