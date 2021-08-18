from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://www.hko.gov.hk/textonly/v2/forecast/chinesewx2.htm')
weather = r.html.xpath('//*[@id="ming"]/text()', first=True)
print(weather)


