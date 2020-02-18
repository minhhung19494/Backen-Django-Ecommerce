# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
# from scrapy.contrib.djangoitem import DjangoItem

edit_price = MapCompose( lambda price: float(price.split(' ')[0].replace(',','')))
edit_slug = MapCompose (lambda slug : slug.split('/')[-1])
edit_image_urls = MapCompose(lambda image_url : 'http:' + image_url)
# edit_description = MapCompose(lambda str: str.replace('\"' , ' ' ))

class Product(scrapy.Item):
    name = scrapy.Field(
        input_processor = MapCompose(remove_tags)
    )
    category = scrapy.Field(
        input_processor = MapCompose(remove_tags)
    )
    image_urls = scrapy.Field(
        input_processor = edit_image_urls
    )
    images = scrapy.Field()
    price = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = edit_price
    )
    slug = scrapy.Field(
        input_processor = edit_slug
    )
    label = scrapy.Field()
    description = scrapy.Field()
class ProductVariations(scrapy.Item):
    itemName = scrapy.Field(
        input_processor = MapCompose(remove_tags)
    )
    variation = scrapy.Field(
        input_processor = MapCompose(remove_tags)
    ) # size or color
    value = scrapy.Field(
        input_processor = MapCompose(remove_tags)
    ) # S, M, L
    image_urls = scrapy.Field(
        input_processor = edit_image_urls
    ) #Image
    images = scrapy.Field()
    description = scrapy.Field(
        # input_processor = MapCompose(remove_tags),
        ouput_processor = Join()
    )
class ProductDescription(scrapy.Item):
    itemName = scrapy.Field(
        input_processor = MapCompose(remove_tags)
    )
    description = scrapy.Field()
