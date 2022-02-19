import scrapy


class WildberriesItem(scrapy.Item):
    id = scrapy.Field()
    inn = scrapy.Field()
    supplierId = scrapy.Field()
    supplierName = scrapy.Field()
    legalAddress = scrapy.Field()
    name = scrapy.Field()
    brand = scrapy.Field()
    priceU = scrapy.Field()
    sale = scrapy.Field()
    salePriceU = scrapy.Field()
    pics = scrapy.Field()
    colors = scrapy.Field()
    sizes = scrapy.Field()
    qty = scrapy.Field()
    diffPrice = scrapy.Field()
    price_history = scrapy.Field()
    rating = scrapy.Field()
    comments = scrapy.Field()
    sold = scrapy.Field()
    description = scrapy.Field()
    questions = scrapy.Field()

