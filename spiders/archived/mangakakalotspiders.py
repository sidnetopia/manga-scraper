from datetime import datetime
import re

import requests

from manga_scraper.items import Manga, Chapter
import scrapy


class MangakakalotSpidersOld(scrapy.Spider):
    name = "mangakakalot-spider-old"
    start_urls = ["https://chapmanganato.com/manga-ei981691"]
    title_pattern = r'Chapter\s+(\d+)(?::\s+(.+))?'

    def parse_date(self, pub_date):
        pub_date = datetime.strptime(pub_date, "%b %d,%Y %H:%M")
        pub_date = int(pub_date.timestamp())

        return pub_date

    def parse_title_info(self, title):
        # Search for the pattern in the string
        match = re.search(self.title_pattern, title)

        # Extract the first and second groups of the match
        chap_num = match.group(1)
        title = match.group(2) if match.group(2) else ''

        return chap_num, title

    def parse(self, response):
        chapter_hrefs = response.xpath('//li[@class="a-h"]')[:1]
        manga_title = response.xpath('//div[@class="story-info-right"]/h1/text()').get()

        session_vars = response.request.headers.getlist('Cookie')
        print("session_vars", session_vars)
        manga = Manga(title=manga_title)
        chapters = []
        for chapter_href in chapter_hrefs:
            pub_date = chapter_href.xpath('.//span[@class="chapter-time text-nowrap"]/@title').get()
            pub_date = self.parse_date(pub_date)

            hyperlink = chapter_href.xpath('.//a')
            chap_title_raw = hyperlink.xpath('@title').get()

            chap_num, title = self.parse_title_info(chap_title_raw)
            link = hyperlink.xpath('@href').get()

            chapter = Chapter(title=title, pub_date=pub_date, chap_num=chap_num)
            chapters.append(chapter)

            yield scrapy.Request(link, callback=self.parse_chapter, meta={"manga": manga, "chapter": chapter})

        manga['chapters'] = chapters

    def parse_chapter(self, response):
        manga = response.meta["manga"]
        chapter = response.meta["chapter"]

        img_urls = response.xpath('//div[@class="container-chapter-reader"]/img/@src')
        yield from response.follow_all(img_urls, self.parse_img)
        chapter['img_urls'] = img_urls.getall()

        manga['chapters'] = [c for c in manga['chapters'] if c != chapter]
        manga['chapters'].append(chapter)

        yield manga

    def parse_img(self, response):
        print(response)