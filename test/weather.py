from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://www.hko.gov.hk/textonly/v2/forecast/chinesewx2.htm')
weather = r.html.xpath("//pre[@id='ming']/text()")
try:
    p = r.html.xpath("//pre[@id='ming']/p/text()", first=True)
except ValueError:
    pass
if " " in p:
    print(weather[0]+p+weather[1])
else:
    print(weather[0]+weather[1])





