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
        chapter_hrefs = response.xpath('//div[@class="slide-caption"]/h3/a').getall()
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