#!/usr/bin/env python
# checks new offers on olx.ua/slando.ua and shows them as desktop notifications
from lxml import html
import requests
import pynotify
import tempfile
import os
from time import sleep

pynotify.init('MsgNotification')
offers_history = []

def notification(title, body, url, image=None):
    if image is not None:
        r = requests.get(image)
        tf = tempfile.NamedTemporaryFile(prefix="slando",delete=False)
        with open(tf.name, 'w+b') as f:
          f.write(r.content)
          f.close()
        notification = pynotify.Notification(title, body, tf.name)
    else:
        notification = pynotify.Notification(title, body)
    notification.set_urgency(pynotify.URGENCY_LOW)
    notification.set_timeout(pynotify.EXPIRES_DEFAULT)
    notification.show()
    #os.remove(tf.name)

while True:
    page = requests.get('http://kiev.ko.olx.ua/hobbi-otdyh-i-sport/sport-otdyh/velo/')
    tree = html.fromstring(page.text)
    offers = tree.xpath('//table[contains(@class,"fixed breakword")]')

    for o in offers:
        imagelist = o.xpath('.//img[@class="fleft"]/@src')
        if len(imagelist) > 0:
            image = imagelist[0]
        else:
            image = None
        url = o.xpath('.//a[@class="marginright5 link linkWithHash detailsLink"]/@href')[0]
        title = o.xpath('.//a[@class="marginright5 link linkWithHash detailsLink"]/strong/text()')[0]
        price = o.xpath('.//p[@class="price"]/strong/text()')[0]
        flag = True
        for h in offers_history:
            if h['title'].lower() == title.lower():
                flag = False
                break
        if flag:
            offers_history += [{'image': image, 'url': url, 'title': title, 'price': price}]
            print("Added {}".format(title))
            htmlbody = '<a href="{}">{}</a>'.format(url,title,price)
            notification(price, htmlbody, url, image)
    sleep(5)
