import scrapy
import logging
import urllib.parse

from manga_scraper.spiders.mangakakalot_manga_spiders import MangakakalotMangaSpiders
from manga_scraper.spiders.manganeto_manga_spiders import ManganetoMangaSpiders
from manga_scraper.utils import MangakakalotManga as MangakakalotMangaUtils

logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(levelname)s] %(message)s', filename='log.txt', level=logging.ERROR)


class MangakakalotSpiders(scrapy.Spider):
    name = "mangakakalot-spider"
    main_url = "https://mangakakalot.com/manga_list?category=all&state=all&page={}"

    def __init__(self):
        super().__init__()
        self.mangakakalot_manga_spiders = MangakakalotMangaSpiders()
        self.manganeto_manga_spiders = ManganetoMangaSpiders()

    def start_requests(self):
        yield scrapy.Request(url=self.main_url.format(1), callback=self.parse)

    def parse(self, response):
        title_links = response.xpath('//div[@class="list-truyen-item-wrap"]//h3/a/@href').getall()

        for title_link in title_links:
            parsed_link = urllib.parse.urlparse(title_link)
            if parsed_link.netloc == 'mangakakalot.com':
                spider_method = self.mangakakalot_manga_spiders.parse_manga
            else:
                spider_method = self.manganeto_manga_spiders.parse_manga

            yield scrapy.Request(title_link, spider_method)
        
        num_pages = response.xpath('//a[@class="page_blue page_last"]/text()').extract_first()
        num_pages = MangakakalotMangaUtils.get_page_num(num_pages)

        # num_pages = 2
        for page in range(2, num_pages + 1):
            next_page = self.main_url.format(page)
            yield response.follow(url=next_page, callback=self.parse)
