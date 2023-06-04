from datetime import datetime
import re

import requests

from manga_scraper.items import Manga, Chapter
import scrapy
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

class MangakakalotTitleSpiders(scrapy.Spider):
    name = "mangakakalot-title-spider"
    main_url = "https://mangakakalot.com/manga_list?category=all&state=all&page={}"

    def start_requests(self):
        yield scrapy.Request(url=self.main_url.format(1), callback=self.parse)

    def parse(self, response):
        for link in  response.xpath('//div[@class="slide-caption"]//h3/a/@href'):
        logger.info("response: %s", response)
        yield {'links':.getall()}

        for page in range(2, 3 + 1):
            yield scrapy.Request(url=self.main_url.format(page), callback=self.parse)