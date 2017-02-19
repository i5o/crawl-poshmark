# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    """
    Main class for a product, contains all the fields == data.
    """
    images = scrapy.Field()
    image_urls = scrapy.Field()
    id_ = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    size = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    subsubcategory = scrapy.Field()
    colors = scrapy.Field()
    price = scrapy.Field()
