# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy import Request


class MobileSpider(scrapy.Spider):
    name = 'mobile'
    allowed_domains = ['www.flipkart.com']
    start_urls = ['https://www.flipkart.com/mobiles/mi~brand/pr?sid=tyy,4io&otracker=nmenu_sub_Electronics_0_Mi']

    # def start_requests(self):
    #      url="https://www.flipkart.com/mobiles/mi~brand/pr?sid=tyy,4io&otracker=nmenu_sub_Electronics_0_Mi"
    #      yield SplashRequest(url)
        
    def parse(self, response):
        product_selector = response.xpath("//div[@class='_2kHMtA']")
        
        for product in product_selector:
            yield {
              'title' : product.xpath(".//div[@class='_4rR01T']/text()").get(),
              'link'  : response.urljoin(product.xpath(".//@href").get()),
              'price' : product.xpath(".//div[@class='_30jeq3 _1_WHN1']/text()").get()
                 }
        next_page = response.xpath("//a[@class='_1LKTO3']") 
        for page in next_page:
            absolute_page = response.urljoin(page.xpath(".//href").get())

            yield scrapy.Request(url = absolute_page, callback=self.parse)
          
        