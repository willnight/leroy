import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pprint import pprint
import pymongo
import hashlib
from scrapy.utils.python import to_bytes


class LeroymerlinPipeline:
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.mongodb = client['leroymerlin_db']

    def process_item(self, item, spider):
        item['description'] = description_to_dict(item['description'])
        collection = self.mongodb[spider.name]
        collection.find_and_modify({"link": item['link']}, {"$set": item}, upsert=True)
        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        photos_set = set(item['photos'])
        # pprint(photos_set)
        if photos_set:
            for img in photos_set:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        item_name = item['name']
        return f'full/{item_name}/{image_guid}.jpg'


def description_to_dict(value):
    res_dist = {}
    for i, item in enumerate(value):
        if i % 2 == 0:
            res_dist[value[i]] = value[i + 1]
    return res_dist
