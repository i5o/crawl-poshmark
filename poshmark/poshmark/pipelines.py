# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
import os
settings = get_project_settings()
path = settings.get("CAT_PATH")


class ProductImage(ImagesPipeline):
    """
    Downloads the images of the product
    Enable it on settings.py
    """

    def file_path(self, request, response=None, info=None):
        """
        Returns the file name based on the product id -- image file name.
        """
        product_id = request.meta['id_'][0]
        filename = request.url.split('/')[-1]

        if not os.path.exists(path):
            os.mkdir(path)

        if not os.path.exists("%s/%s" % (path, product_id)):
            os.mkdir("%s/%s" % (path, product_id))

        return '%s/%s/%s' % (path, product_id, filename)

    def get_media_requests(self, item, info):
        """
        Creates scrapy requests based on the urls of the images.
        """
        for url in item.get('image_urls'):
            yield Request(url, meta=item)

    def item_completed(self, results, item, info):
        """
        Once the download is completed that's reported and saved on item["images"]
        """
        item['images'] = [x for ok, x in results if ok]
        return item
