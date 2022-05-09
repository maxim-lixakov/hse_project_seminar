import re

import scrapy

SUCCESS_CODES = [200, 201]


class SitemapSpider(scrapy.Spider):
    name = 'sitemap'
    allowed_domains = ['www.wildberries.ru']
    parsed_catalogs = set()

    def start_requests(self):
        yield scrapy.Request(url='https://www.wildberries.ru/data', callback=self.parse_catalog, method='POST')

    def parse_catalog(self, response):
        # catalogs = response.xpath('//a[contains(@href, "catalog")]/@href').getall()
        # self.parsed_catalogs.update(catalogs)
        # for catalog in self.parsed_catalogs:
        #     yield scrapy.Request(url=catalog, callback=self.parse)
        data = response.json()['value']['data']
        for link in data['mainBanners']:
            yield scrapy.Request(url='https://www.wildberries.ru'+link['link'])

    def parse(self, response, **kwargs):
        goods = response.xpath('//a[contains(@href, "detail.aspx")]/@href').getall()
        for good in goods:
            yield {'url': good}
        next_page = int(response.xpath('//span[contains(@class, "active")]/text()').get()) + 1
        yield scrapy.Request(url=re.sub(
            'page=\d*', 'page='+ str(next_page),
            response.url), callback=self.parse)