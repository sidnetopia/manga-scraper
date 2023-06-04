from datetime import datetime
import re

import requests

from manga_scraper.items import Manga, Chapter
import scrapy



class MangakakalotTitleSpiders(scrapy.Spider):
    name = "mangakakalot-title-spider"
    start_urls = [
        # "https://mangakakalot.com/manga_list?type=latest&category=all&state=all&page=1",
        "https://mangakakalot.com/manga_list?type=topview&category=all&state=all&page=1",
        "https://mangakakalot.com/manga_list?type=newest&category=all&state=all&page=1",
        "https://mangakakalot.com/manga_list?type=newest&category=all&state=Completed&page=1"
    ]

    def parse(self, response):
        title_links = response.xpath('//div[@class="slide-caption"]/h3/a/@href').getall()
        print(title_links)
        # for title_link in title_links:
        #     pass
        
        next_page = response.xpath('//div[@class="group_page"]/a[not(@class)]/@href').extract_first()
        num_pages = json_response['info'].get('pages')
        for page in range(2, num_pages + 1):
            next_page = f'https://rickandmortyapi.com/api/character/?page={page}'
            yield response.follow(next_page, callback=self.parse)
        yield response.follow(next_page, callback=self.parse)