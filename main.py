import os
from dotenv import load_dotenv
import telebot
from requests_html import HTMLSession
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from geopy.geocoders import Nominatim
from geopy.point import Point
from functools import partial

# Setup Bot Token
load_dotenv()
API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)


def getChatID(message):
    return message.chat.id


def introMarkup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("目前天氣"), KeyboardButton("目前交通消息"))
    markup.add(KeyboardButton("目前位置轉換為文字", request_location=True))
    return markup


@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_message(getChatID(message), text="請選擇功能", reply_markup=introMarkup())


@bot.message_handler(func=lambda message: message.text == "目前天氣")
def getWeather(message):
    result = ""
    session = HTMLSession()
    r = session.get("https://www.hko.gov.hk/textonly/v2/forecast/chinesewx2.htm")
    weather = r.html.xpath("//pre[@id='ming']/text()")
    otherInfo = r.html.xpath("//*[@id='ming']/p[1]/text()", first=True)
    for text in weather:
        try:
            if text == weather[1]:
                result += otherInfo
        except IndexError:
            pass
        result += text
    bot.reply_to(message, result, reply_markup=introMarkup())


@bot.message_handler(content_types=["location"])
def getLocation(message):
    longitude = message.location.longitude
    latitude = message.location.latitude
    geolocator = Nominatim(user_agent="twmostBot")
    reverse = partial(geolocator.reverse, language="zh")
    location = reverse(Point(latitude, longitude))
    bot.reply_to(
        message,
        text="讀取成功，目前位置為:",
        reply_markup=introMarkup(),
    )
    bot.send_message(getChatID(message), location)


@bot.message_handler(func=lambda message: message.text == "目前交通消息")
def getCarInfo(message):
    session = HTMLSession()
    today = datetime.today().date()
    today = str(today).split("-")
    web = (
        "https://programme.rthk.hk/channel/radio/trafficnews/index.php?d={}{}{}".format(
            today[0], today[1], today[2]
        )
    )
    r = session.get(web)
    article = r.html.xpath('//*[@id="content"]/div/ul')
    article_rev = []
    carInfo = ""
    if article == []:
        carInfo = "Currently no news."
    else:
        for news in article:
            article_rev.insert(0, news)

        for info in article_rev[-10:]:
            carInfo += info.text + "\n\n"
    bot.reply_to(message, carInfo, reply_markup=introMarkup())


bot.infinity_polling(timeout=10, long_polling_timeout=5)
