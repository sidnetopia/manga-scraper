# import the necessary packages

import scrapy

class Chapter(scrapy.Item):
	title = scrapy.Field()
	title_info = scrapy.Field()
	chapter_number = scrapy.Field()
	time_uploaded = scrapy.Field()
	views = scrapy.Field()
	url = scrapy.Field(output_processor=[])

class MangaRating(scrapy.Item):
	rating = scrapy.Field()
	num_votes = scrapy.Field()

class Manga(scrapy.Item):
	url = scrapy.Field()
	standing = scrapy.Field()
	title = scrapy.Field()
	alternative_titles = scrapy.Field()
	thumbnail_url = scrapy.Field()
	authors = scrapy.Field(output_processor=[])
	status = scrapy.Field()
	last_updated_at = scrapy.Field()
	genres = scrapy.Field()
	rating = scrapy.Field()
	view_count = scrapy.Field()
	summary = scrapy.Field()
	chapters = scrapy.Field(output_processor=[])