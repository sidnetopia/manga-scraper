from datetime import datetime
import re

import requests

from manga_scraper.items import Manga, Chapter
import scrapy



class MangakakalotTitleSpiders(scrapy.Spider):
    name = "mangakakalot-title-spider"
    main_url = "https://mangakakalot.com/manga_list?category=all&state=all&page={}"

    def start_requests(self):
        yield scrapy.Request(url=self.main_url, callback=self.parse)

    def parse(self, response):
        title_links = response.xpath('//div[@class="slide-caption"]/h3/a/@href').getall()
        print(title_links)
        # for title_link in title_links:
        #     pass
        
        num_pages = response.xpath('//a[@class="page_blue page_last"]').extract_first()
        num_pages = re.search(r'\d+', num_pages).group()
        for page in range(2, num_pages + 1):
            next_page = f'https://rickandmortyapi.com/api/character/?page={page}'
            yield response.follow(next_page, callback=self.parse)
        yield response.follow(next_page, callback=self.parse)