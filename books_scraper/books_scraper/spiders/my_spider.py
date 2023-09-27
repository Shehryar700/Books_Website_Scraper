import scrapy
from books_scraper.items import BooksScraperItem

class MySpider(scrapy.Spider):
    name = "Books_Details"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        category_links = response.css('div.side_categories > ul > li > ul > li > a')
        for genre in category_links:
            category_name = genre.css('::text').get().strip()
            yield response.follow(genre.attrib['href'], callback=self.parse_category, meta={'category_name': category_name})

    def parse_category(self, response):
        category_name = response.meta['category_name']
        book_links = response.css('h3 > a::attr(href)').getall()

        for book_link in book_links:
            yield response.follow(book_link, callback=self.parse_book, meta={'category_name': category_name})

        next_page = response.css('li.next > a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_category, meta={'category_name': category_name})
    def parse_book(self, response):

        item = BooksScraperItem()
        item['category'] = response.meta['category_name']
        item['name'] = response.css('div>h1::text').get("").strip()
        item['description'] = response.css('meta[name="description"]::attr(content)').get("").replace("...more", "").strip()
        item['upc'] = response.css('th:contains("UPC") + td::text').get("").strip()
        item['price_tax_exc'] = response.css('th:contains("Price (excl. tax)") + td::text').get("").replace("£", "").strip()
        item['price_tax_inc'] = response.css('th:contains("Price (incl. tax)") + td::text').get("").replace("£", "").strip()
        item['availability'] = response.css('th:contains("Availability") + td::text').get("").strip()
        item['reviews'] = response.css('th:contains("Number of reviews") + td::text').get("").strip()

        yield item
