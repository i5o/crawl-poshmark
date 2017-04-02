# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from links import links

template = """# -*- coding: utf-8 -*-
import os
BOT_NAME = 'poshmark'
SPIDER_MODULES = ['poshmark.spiders']
NEWSPIDER_MODULE = 'poshmark.spiders'
USER_AGENT = "Mozilla/5.0 (X11; CrOS armv7l 9280.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3007.0 Safari/537.36"
ITEM_PIPELINES = {'poshmark.pipelines.ProductImage': 1}
LINK = "XXX"
CAT_PATH = "YYY"
"""


for link in links.keys():
    for subsub in links[link]:
        CAT_PATH = "data/%s/%s/" % (link, subsub[0]) # data/SubCat/SubSubCat/images
        f = open("poshmark/settings.py", "w")
        f.write(template.replace("XXX", subsub[1]).replace("YYY", CAT_PATH))
        f.close()
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        process.crawl('products')
        process.start()
        break
