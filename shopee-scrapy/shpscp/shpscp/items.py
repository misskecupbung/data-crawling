# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def fix_price(price):
    return int(price/100000)


class ShpscpItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field(output_processor=TakeFirst(),)
    name = scrapy.Field(output_processor=TakeFirst(),)
    price = scrapy.Field(input_processor=MapCompose(fix_price,), output_processor=TakeFirst(),)
    sold = scrapy.Field(output_processor=TakeFirst(),)
    categori = scrapy.Field(output_processor=TakeFirst(),)
    rate = scrapy.Field(output_processor=TakeFirst(),)
    place = scrapy.Field(output_processor=TakeFirst(),)
