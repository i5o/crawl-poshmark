# -*- coding: utf-8 -*-
import os
import sys
import re
from scrapy import signals
from scrapy import Spider
from scrapy import Request
from scrapy.loader import ItemLoader
from poshmark.items import Product
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from datetime import datetime

class ProductsSpider(Spider):
    """
    The main spider class. Contains all the functions required to crawl
    the website.
    """
    name = "products"
    max_pages = 50 # Set this to 0 to remove the limit
    current_page = 1
    items = []

    def __init__(self):
        dispatcher.connect(self.crawl_over, signals.spider_closed)

    def crawl_over(self, spider):
        # The script is over, so lets write the csv data. Just in case :)
        self.create_csv_file()
        self.log("script over --> CSV file created.")

    def start_requests(self):
        """
        Creates a request with the website_url, then the data is analyzed
        by self.parse
        """
        website_url = settings.get("LINK")
        yield Request(url=website_url, callback=self.parse)
        pass

    def parse(self, response):
        """
        Finds all the products, and then recovers the data by calling
        self.parse_product_data; it also checks that the max_page limit
        is respected

        All the products have a div with the class "col-x12 col-l6 col-s8"
        """
        products = response.xpath('//div[@class="col-x12 col-l6 col-s8"]')

        for product in products:
            # Creates a request with the product url, then the data of the website
            # is analyzed by self.parse_product_data.
            product_link = "https://poshmark.com" + product.xpath(
                './/a[@class="covershot-con"]/@href').extract()[0]

            yield Request(url=product_link, callback=self.parse_product_data)

        # If we are in a page that is multiple of 20, lets write the csv data.
        if not (self.current_page % 20):
            print("Page multiple of 20 -- %s" % datetime.strftime(datetime.now(), "%c"))
            self.log("--> page multiple of 20")
            self.create_csv_file()
            self.log("--> CSV file created")

        if (self.max_pages == self.current_page):
            return

        self.current_page += 1
        print("self.current_page has increased (it's %d)" %
            self.current_page)

        # Creates the next page url
        # https://poshmark.com//category/Women?max_id=[next_page]
        # &sort_by=price_asc
        next_url = "%s?max_id=%d&sort_by=price_asc" % (settings.get("LINK"), self.current_page)

        # Simple recursion. Calls self.parse with the Next page url.
        yield Request(url=next_url, callback=self.parse)

    def parse_product_data(self, response):
        """
        Obtains the whole data about products.
        Each variable has it own name (so you should be able to identify the things)
        How it works:
        product_something = response.xpath(**xpath**)
        Basically it finds the element that has the data we are looking for.
        """

        product_id = response.url.split("-")[-1]
        product_url = response.url

        # If the product_id is the same as the product_url, then the content
        # after https://poshmark.com/listing/ is the id
        if product_id == product_url:
            product_id = product_url.split("/")[-1]

        print(settings.get("CAT_PATH"), product_url)

        product_title = response.xpath(
            '//h1[@class="title"]/text()').extract()[0]
        product_description = response.xpath(
            '//div[@class="description"]/text()').extract()[0]

        try:
            product_size = response.xpath(
                '//div[@class="multi-size"][1]/label/div/text()').extract()
        except:
            product_size = response.xpath(
                '//div[@class="multi-size"][0]/label/div/text()').extract()

        product_size = ", ".join(list(set(product_size)))
        product_categories = response.xpath(
            '//div[@class="tag-list"]/a[@class="tag"][not(@data-pa-name="listing_details_color")]/text()').extract()

        product_category = product_categories[0]
        product_subcategory = ""
        product_subsubcategory = ""

        if len(product_categories) > 1:
            product_subcategory = product_categories[1]

        if len(product_categories) > 2:
            product_subsubcategory = product_categories[2]

        product_colors = ", ".join(response.xpath(
            '//a[@class="tag"][@data-pa-name="listing_details_color"]/text()').extract())
        product_price = response.xpath(
            '//div[@class="price"]/text()').extract()[0][:-1]

        if not product_colors:
            product_colors = "No color category"

        # Later, an ItemLoader is created. Which basically contains all the
        # data of the product
        # The obtained data is added to this item
        item = ItemLoader(item=Product(), response=response)
        item.add_value('id_', product_id)
        item.add_value('url', product_url)
        item.add_xpath(
            'image_urls',
            '//div[contains(@class, "image-con")]/img/@src')
        item.add_value('title', product_title)
        item.add_value('description', product_description)
        item.add_value('size', product_size)
        item.add_value('category', product_category)
        item.add_value('subcategory', product_subcategory)
        item.add_value('subsubcategory', product_subsubcategory)
        item.add_value('colors', product_colors)
        item.add_value('price', product_price)

        # Once all the data is added, we call "load_item", which basically
        # will call the pipeline to download of images /if enabled/
        loaded_item = item.load_item()
        self.items.append(dict(loaded_item))

        return loaded_item

    def create_csv_file(self):
        txt = """id, url, title, description, size, category, subcategory, colors, price, image urls
"""
        sorted_items = sorted(
            self.items,
            key=lambda x: (
                x["category"],
                x["subcategory"],
                x["subsubcategory"]))
        for item in sorted_items:
            # Replace new lines for two spaces
            # and due to restrictions with csv replace " for ''

            myre = re.compile(u'['
                 u'\U0001F300-\U0001F64F'
                 u'\U0001F680-\U0001F6FF'
                 u'\u2600-\u26FF\u2700-\u27BF]+',
                 re.UNICODE)

            description = item["description"][0]
            description = description.replace('"', "'")
            description = description.replace('\n', "  ")
            description = myre.sub('', description)
            title = item["title"][0].replace('\n', "  ")
            title = myre.sub('', title)
            size = item["size"][0]
            size = size.replace('"', "''")

            txt += '''"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"
''' % (item["id_"][0], item["url"][0], title, description,
                size, item["subcategory"][0], item["subsubcategory"][0],
                item["colors"][0], item["price"][0],
                ", ".join(item["image_urls"]))

            csv_file = open("%s/products.csv" % settings.get("CAT_PATH"), "wb")
            csv_file.write(txt.encode("utf-8"))
            csv_file.close()
