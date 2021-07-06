import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def change_url(value):
    try:
        pic_name = value[value.rfind('/', 0, len(value)) + 1:]
        result = f'https://res.cloudinary.com/lmru/image/upload/LMCode/{pic_name}'
        return result
    except Exception:
        return value


def clear(value):
    try:
        result = value.replace('\n', ' ')
        return result
    except Exception:
        return value


def clear_description(value):
    try:
        result = value.replace('\n', ' ').strip()
        return result
    except Exception:
        return value


def clear_price(value):
    try:
        result = int(value.replace(' ', '').strip())
        return result
    except Exception:
        return value


class LeroymerlinItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(clear), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(change_url))
    description = scrapy.Field(input_processor=MapCompose(clear_description))
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    updated = scrapy.Field(output_processor=TakeFirst())

