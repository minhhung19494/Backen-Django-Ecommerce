# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy_app.items import Product, ProductVariations
from scrapy.crawler import CrawlerProcess

class ProductCrawler(scrapy.Spider):
    name = 'icrawler'
    # allowed_domains = ['https://bitis.com.vn/']
    start_urls = ['https://bitis.com.vn/collections/hunter-nam/']

    # def __init__(self, *args, **kwargs):
    #     # self.url = kwargs.get('url')
    #     # self.domain = kwargs.get('domain')
    #     self.start_urls = ['https://bitis.com.vn/collections/hunter-nam/']
    #     # self.allowed_domains = [self.domain]

    #     ProductCrawler.rules = [
    #         Rule(LinkExtractor(unique=True), callback='parse'),
    #     ]
    #     super(ProductCrawler, self).__init__(*args, **kwargs)

    def parse(self, response):

        productLoader = ItemLoader(item = Product(), response = response)
        yield self.startProductLoader(response, productLoader)

        detailPages = response.css('h3.product_name a::attr(href)').getall()
        for page in detailPages:
            yield scrapy.Request(
                response.urljoin(page),
                callback= self.parseDetailPage
        )

        next_page = response.css('div#pagination a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(
                next_page, 
                callback=self.parse
            )

    def startProductLoader(self, response, productLoader):

        productLoader = ItemLoader(item = Product(), response = response)

        productLoader.add_css('name', 'h3.product_name a')
        productLoader.add_css('category', 'div.product_category a')
        productLoader.add_css('image_urls', 'img.image_main::attr(src)')
        productLoader.add_css('price', 'span.price')
        productLoader.add_css('slug', 'h3.product_name a::attr(href)')
        productLoader.add_value('label', 'primary')
        productLoader.add_value('description', '')
        
        return productLoader.load_item() 
    
    def parseDetailPage(self,response):
        filterVariation = response.css('div.swatch::attr(data-option-index)').getall()
        print(filterVariation)
        for filter in filterVariation:
            yield self.parseVariation(response, filter)

    def parseVariation(self,response, filter):
        variationLoader = ItemLoader(item = ProductVariations(), response = response)

        variationLoader.add_css('itemName', 'div.product-info h1.name')
        variationLoader.add_css('variation',f'div.swatch[data-option-index = "{filter}"] label.header')
        variationLoader.add_css('value', f'div.swatch[data-option-index = "{filter}"] span::attr(data-value)')
        variationLoader.add_css('image_urls', f'div.swatch[data-option-index = "{filter}"] span img::attr(src)')

        return variationLoader.load_item()
