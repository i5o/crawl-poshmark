# -*- coding: utf-8 -*-

# Scrapy settings for poshmark project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import os

BOT_NAME = 'poshmark'
SPIDER_MODULES = ['poshmark.spiders']
NEWSPIDER_MODULE = 'poshmark.spiders'

# Uncomment this to enable the download of images.
# ITEM_PIPELINES = {'poshmark.pipelines.ProductImage': 1}
# IMAGES_STORE = os.getcwd()
