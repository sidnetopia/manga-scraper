from datetime import datetime
import re

import requests

from manga_scraper.items import Manga, Chapter
import scrapy


class MangakakalotTitleSpiders(scrapy.Spider):
    name = "mangakakalot-title-spider"
    start_urls = [
        "https://mangakakalot.com/manga_list?type=latest&category=all&state=all&page=1",
        "https://mangakakalot.com/manga_list?type=topview&category=all&state=all&page=1",
        "https://mangakakalot.com/manga_list?type=newest&category=all&state=all&page=1",
        "https://mangakakalot.com/manga_list?type=newest&category=all&state=Completed&page=1"
    ]

    def parse(self, response):
        title_links = response.xpath('//div[@class="slide-caption"]/h3/a').getall()

        for title_link in title_links:
            pass
        
        next_page = response.css('//div[@class="group_page"]/a:not([class])::attr(href)').get()    