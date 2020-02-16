# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from core.models import Item, ItemVariation, Variation 
from scrapy_app.items import Product, ProductVariations

class ScrapyAppPipeline(object):
    def __init__(self):
        self.productItems = []
        self.variations = []
    def process_item(self, item, spider):
        if isinstance(item , Product):
            self.productItems.append(item)
        if isinstance(item, ProductVariations):
            self.variations.append(item)
        return item

    def close_spider(self, spider):
        num_page = len(self.productItems)
        for page in range(num_page):
            num_item = len(self.productItems[page]['name'])
            for i in range(num_item):
                new_Item = Item()
                new_Item.title = self.productItems[page]['name'][i]
                new_Item.image = self.productItems[page]['images'][i]['path']
                new_Item.category = self.productItems[page]['category'][i]
                new_Item.price = self.productItems[page]['price'][i]
                new_Item.slug = self.productItems[page]['slug'][i]
                new_Item.description = self.productItems[page]['description'][0]
                new_Item.label = self.productItems[page]['label'][0]
                new_Item.save()

        num_variation = len(self.variations)
        for vari in range(num_variation):
            curr_vari = self.variations[vari]
            num_variationValue = len(curr_vari['value'])
            new_variation = Variation()
            new_variation.item = Item.objects.filter(title = curr_vari['itemName'][0]).first()
            new_variation.name = curr_vari['variation'][0] 
            new_variation.save()
            for j in range(num_variationValue):

                new_variationValue = ItemVariation()
                new_variationValue.variation = new_variation
                new_variationValue.value = curr_vari['value'][j]
                new_variationValue.attachment = curr_vari['images'][j]['path'] if (len(curr_vari['images'])-1)>=j else ''
                new_variationValue.save()

