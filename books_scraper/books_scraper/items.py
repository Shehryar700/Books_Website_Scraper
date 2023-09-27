import scrapy


class BooksScraperItem(scrapy.Item):
    category = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    upc = scrapy.Field()
    price_tax_inc = scrapy.Field()
    price_tax_exc = scrapy.Field()
    availability = scrapy.Field()
    reviews = scrapy.Field()