from datetime import datetime
import re

import requests

from manga_scraper.items import Manga, Chapter
import scrapy

import logging
from scrapy.utils.log import configure_logging

# Define a custom logging format with colors
LOG_FORMAT = '\033[1;30m%(asctime)s\033[0m [%(name)s] \033[%(levelname)s;30m%(levelname)s\033[0m: %(message)s'

# Set the logging level to INFO
logging.basicConfig(level=logging.INFO)

# Configure Scrapy logging with the custom format
configure_logging(install_root_handler=False)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().handlers[0].setFormatter(logging.Formatter(LOG_FORMAT))

class MangakakalotTitleSpiders(scrapy.Spider):
    name = "mangakakalot-title-spider"
    start_urls = [
        "https://mangakakalot.com/manga_list?type=latest&category=all&state=all&page=1",
        "https://mangakakalot.com/manga_list?type=topview&category=all&state=all&page=1",
        "https://mangakakalot.com/manga_list?type=newest&category=all&state=all&page=1",
        "https://mangakakalot.com/manga_list?type=newest&category=all&state=Completed&page=1"
    ]

    def parse(self, response):
        title_links = response.xpath('//div[@class="slide-caption"]/h3/a/@href').getall()
        print(title_links)
        for title_link in title_links:
            pass
        
        next_page = response.css('//div[@class="group_page"]/a[not(@class)]/@href').get()
        print("next_page", next_page)
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)