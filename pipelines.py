# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import quote
from scrapy.exceptions import DropItem
from scrapy import Request

class ChapterImagesPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        chapters = adapter["chapters"]

        for chapter in chapters:
            chap_num = chapter['chap_num']
            img_urls = chapter['img_urls']

            for img_url in img_urls:
                encoded_img_url = quote(img_url)

    # def file_path(self, request, response=None, info=None):
    #     print("file_path")
    #     print("request", request)
    #     print("response", response)
    #     print("info", info)
    #     # url = request.url
    #     # file_name = url.split('/')[-1]
    #     # return file_name
    #
    # def item_completed(self, results, item, info):
    #     print("item_completed")
    #     print("results", results)
    #     print("item", item)
    #     print("info", info)
    #     # image_paths = [x['path'] for ok, x in results if ok]
    #     # if not image_paths:
    #     #     raise DropItem('Image Downloaded Failed')
    #     # return item
    #
    # def get_media_requests(self, item, info):
    #     print("get_media_requests")
    #     print("item", item)
    #     print("info", info)
    #     # yield Request(item['url'])
