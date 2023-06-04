import scrapy
from manga_scraper.utils import MangakakalotManga as MangakakalotMangaUtils, MangakakalotChapter as MangakakalotChapterUtils
from manga_scraper.items import Manga, MangaRating, Chapter

class ManganetoMangaSpiders(scrapy.Spider):
    name = "manganeto-manga-spider"

    def __init__(self):
        super().__init__()

    def parse_manga(self, response):
        manga_info = response.xpath('//div[@class="story-info-right"]')
        title = manga_info.xpath('.//h1/text()').extract_first()
        table_info = manga_info.xpath('.//table[@class="variations-tableInfo"]/tbody')

        alt_titles = ''
        authors = ''
        status = ''
        genres = ''
        for table_row in table_info.xpath('./tr'):
            row_name = table_row.xpath('./td[1]/text()').extract_first()
            if 'Alternative' in row_name:
                alt_titles = table_row.xpath('.//h2/text()').extract_first()
                alt_titles = MangakakalotMangaUtils.get_alt_titles(alt_titles)
            elif 'Author' in row_name:
                authors = table_row.xpath('.//a/text()').extract()
            elif 'Status' in row_name:
                status = table_row.xpath('.//td[2]/text()').extract_first()
                status = MangakakalotMangaUtils.get_status(status)
            elif 'Genres' in row_name:
                genres = table_row.xpath('.//a/text()').extract()

        p_info = manga_info.xpath('.//div[@class="story-info-right-extent"]')
        last_updated_at = p_info.xpath('./p[1]/span[2]/text()').extract_first()
        last_updated_at = MangakakalotMangaUtils.get_last_updated_at_timestamp(last_updated_at)
        view_count = p_info.xpath('./p[2]/span[2]/text()').extract_first()
        view_count = MangakakalotMangaUtils.get_view_count(view_count)
        rating_info = p_info.xpath('./p[4]//em[@id="rate_row_cmd"]//text()').extract()
        rating_info = ''.join([elem.replace('\n', '') for elem in rating_info if elem.strip()])
        rating, num_votes = MangakakalotMangaUtils.get_ratings(rating_info)

        summary = response.xpath('//div[@id="panel-story-info-description"]//text()')[2].extract()
        summary = MangakakalotMangaUtils.get_summary(summary)

        thumbnail_url = response.xpath('//span[@class="info-image"]/img/@src').extract_first()

        rating = MangaRating(
            rating=rating,
            num_votes=num_votes
        )

        if response.css('.item-hot'):
            # The class exists in the response
            standing = 'hot'
        elif response.css('.item-ss'):
            standing = 'ss'
        else:
            # The class doesn't exist in the response
            standing = ''

        manga = Manga(
            url=response.url,
            standing=standing,
            title=title,
            alternative_titles=alt_titles,
            authors=authors,
            status=status,
            last_updated_at=last_updated_at,
            view_count=view_count,
            genres=genres,
            rating=rating,
            summary=summary,
            thumbnail_url=thumbnail_url,
            chapters=[]
        )

        chapter_elems = response.xpath('//ul[@class="row-content-chapter"]/li')
        self.parse_chapters(chapter_elems, manga)

        yield manga

    def parse_chapters(self, chapter_elems, manga):
        for elem in chapter_elems:
            a_elem = elem.xpath('.//a')
            url = a_elem.xpath('.//@href').extract_first()
            title_info = a_elem.xpath('.//text()').extract_first()
            chap_num, title = MangakakalotChapterUtils.get_title_info(title_info)
            view_count = elem.xpath('./span[1]/text()').extract_first()
            view_count = MangakakalotChapterUtils.get_view_count(view_count)
            pub_date = elem.xpath('./span[2]/text()').extract_first()
            pub_date = MangakakalotChapterUtils.get_pub_date(pub_date)


            chapter = Chapter(title=title, title_info=title_info, chapter_number=chap_num, time_uploaded=pub_date, views=view_count, url=url)
            manga["chapters"].append(chapter)
