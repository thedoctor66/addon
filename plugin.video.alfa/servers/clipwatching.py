# -*- coding: utf-8 -*-

from core import httptools
from core import scrapertools
from lib import jsunpack
from platformcode import logger, config


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data
    if "File Not Found" in data:
        return False, config.get_localized_string(70292) % "ClipWatching"
    return True, ""


def get_video_url(page_url, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data
    packed = scrapertools.find_single_match(data, "text/javascript'>(.*?)\s*</script>")
    unpacked = jsunpack.unpack(packed)
    video_urls = []
    videos = scrapertools.find_multiple_matches(unpacked, 'file:"([^"]+).*?label:"([^"]+)')
    for video, label in videos:
        video_urls.append([label + " [clipwatching]", video])
    logger.info("Url: %s" % videos)
    video_urls.sort(key=lambda it: int(it[0].split("p ", 1)[0]))
    return video_urls
