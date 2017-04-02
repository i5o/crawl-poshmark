# -*- coding: utf-8 -*-
import os
BOT_NAME = 'poshmark'
SPIDER_MODULES = ['poshmark.spiders']
NEWSPIDER_MODULE = 'poshmark.spiders'
USER_AGENT = "Mozilla/5.0 (X11; CrOS armv7l 9280.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3007.0 Safari/537.36"
ITEM_PIPELINES = {'poshmark.pipelines.ProductImage': 1}
LINK = "https://poshmark.com/category/Women-Dresses-One_Shoulder"
CAT_PATH = "data/Dresses/One Shoulder/"
IMAGES_STORE = os.getcwd()
