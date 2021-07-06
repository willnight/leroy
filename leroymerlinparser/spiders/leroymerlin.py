import scrapy
import requests
from scrapy.http import HtmlResponse
from leroymerlinparser.items import LeroymerlinItem
from scrapy.loader import ItemLoader
from datetime import datetime


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['spb.leroymerlin.ru']

    def __init__(self, search):
        super(LeroymerlinSpider, self).__init__()
        self.page = 1
        self.start_urls = [f'https://spb.leroymerlin.ru/search/?q={search}&page=']

    def parse(self, response: HtmlResponse):
        url = f'{self.start_urls[0]}{self.page}'
        print(url)
        if requests.get(url).ok:
            yield response.follow(url, callback=self.parse)

        product_urls = response.xpath("//a[@data-qa='product-name']/@href")
        for link in product_urls:
            yield response.follow(link, callback=self.parse_product)
        self.page += 1

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)

        loader.add_xpath('name', "//h1[@slot='title']/text()")
        loader.add_xpath('photos', "//picture[@slot='pictures']//source/@srcset")
        loader.add_xpath('description', "//dl[contains(@class,'def-list')]//dt/text() | //dl[contains(@class,'def-list')]//dd/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_value('link', response.url)
        loader.add_value('updated', datetime.now())

        yield loader.load_item()
