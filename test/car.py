from requests_html import HTMLSession
import datetime as dt

session = HTMLSession()

today = dt.date.today()
today = (str(today).split('-'))

#web = "https://programme.rthk.hk/channel/radio/trafficnews/index.php?d={}{}{}".format(today[0],today[1],today[2])
web = "https://programme.rthk.hk/channel/radio/trafficnews/index.php?d=20210815"
r = session.get(web)
article = r.html.xpath('//*[@id="content"]/div/ul')
article_rev = []
carInfo = ""
if article == []:
    carInfo = "Currently no news."
else:
    for i in article:
        article_rev.insert(0,i)


    for info in article_rev[-10:]:
        carInfo += info.text+"\n\n"

print(carInfo)