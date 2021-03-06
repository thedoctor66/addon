# -*- coding: utf-8 -*-

import re
import base64
import urllib

from core import httptools
from core import scrapertools
from lib import jsunpack
from platformcode import logger

headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0']]


def test_video_exists(page_url):
    referer = page_url.replace('iframe', 'preview')
    data = httptools.downloadpage(page_url, headers={'referer': referer}).data
    if data == "File was deleted" or data == '':
        return False, "[powvideo] El video ha sido borrado"
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info()
    itemlist = []

    referer = page_url.replace('iframe', 'preview')

    data = httptools.downloadpage(page_url, headers={'referer': referer}).data

    packed = scrapertools.find_single_match(data, "<script type=[\"']text/javascript[\"']>(eval.*?)</script>")
    unpacked = jsunpack.unpack(packed)
    
    url = scrapertools.find_single_match(unpacked, "(?:src):\\\\'([^\\\\]+.mp4)\\\\'")

    itemlist.append([".mp4" + " [powvideo]", decode_video_url(url)])
    itemlist.sort(key=lambda x: x[0], reverse=True)
    return itemlist

def decode_video_url(url):
    tria = re.compile('[0-9a-z]{40,}', re.IGNORECASE).findall(url)[0]
    gira = tria[::-1]
    x = gira[1:]
    return re.sub(tria, x, url)
