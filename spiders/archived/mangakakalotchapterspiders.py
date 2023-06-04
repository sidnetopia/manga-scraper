from datetime import datetime
import re

from manga_scraper.items import ChapterTest
import scrapy


class MangakakalotChapterSpiders(scrapy.Spider):
    name = "mangakakalot-chapter-spider"
    start_urls = ["https://mangakatana.com/manga/black-clover.257/c358"]

    def parse(self, response):
        print(response.xpath('//div[@id="imgs"]').get())
        imageURLs = response.xpath('//img/@src').getall()
        print(len(imageURLs))
        yield ChapterTest(file_urls=[imageURLs])
