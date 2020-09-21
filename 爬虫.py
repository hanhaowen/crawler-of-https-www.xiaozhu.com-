import requests
from bs4 import BeautifulSoup
import time
import re
import xlwt

wb = xlwt.Workbook()
style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
ws = wb.add_sheet('北京租房')

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/76.0.3809.87 Safari/537.36'}

a = 0


def get_info(url):
    global a
    wb_data = requests.get(url, headers=head)
    soup = BeautifulSoup(wb_data.text, 'html.parser')
    title = soup.find('title')
    addresses = soup.find('span', class_="pr5")
    prices = soup.find('div', class_="day_l")
    ws.write(a, 0, title.get_text().strip(), style0)
    ws.write(a, 1, addresses.get_text().strip(), style0)
    ws.write(a, 2, prices.span.get_text().strip(), style0)
    time.sleep(2)
    a = a + 1


def get_links(url):
    res = requests.get(url, headers=head)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.find_all(href=re.compile("html"))
    for link in links:
        get_info(link['href'])


for i in range(8):
    number = 1
    get_links('http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number))
    number = number + 1

wb.save('example.xls')
