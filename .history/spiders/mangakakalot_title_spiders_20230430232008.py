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
        logger.info("response: %s", response)
        yield {'links': response.xpath('//div[@class="slide-caption"]//h3/a/@href').getall()}

        # for title_link in title_links:
        #     pass
        
        # num_pages = response.xpath('//a[@class="page_blue page_last"]').extract_first()
        # num_pages = re.search(r'\d+', num_pages).group()
        # num_pages = int(num_pages)
        num_pages = 3

        for page in range(2, num_pages + 1):
            next_page = self.main_url.format(page)
            yield scrapy.Request(url=next_page, callback=self.parse)