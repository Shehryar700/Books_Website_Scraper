import scrapy
from books_scraper.items import BooksScraperItem

class MySpider(scrapy.Spider):
    name = "xbot"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        category_links = response.css('div.side_categories > ul > li > ul > li > a')
        for genre in category_links:
            category_name = genre.css('::text').get().strip()
            category_url = response.urljoin(genre.attrib['href'])
            yield response.follow(category_url, callback=self.parse_category, meta={'category_name': category_name})

    def parse_category(self, response):
        category_name = response.meta['category_name']
        book_links = response.css('h3 > a::attr(href)').getall()

        for book_link in book_links:
            book_url = book_link
            yield response.follow(book_url, callback=self.parse_book, meta={'category_name': category_name})

    def parse_book(self, response):
        category_name = response.meta['category_name']
        book_name = response.css('div>h1::text').get()
        book_description = response.css('meta[name="description"]::attr(content)').get().replace("...more", "")
        book_upc = response.css('th:contains("UPC") + td::text').get()
        book_price_excl_tax = response.css('th:contains("Price (excl. tax)") + td::text').get().replace("£", "")
        book_price_incl_tax = response.css('th:contains("Price (incl. tax)") + td::text').get().replace("£", "")
        book_availability = response.css('th:contains("Availability") + td::text').get()
        book_reviews = response.css('th:contains("Number of reviews") + td::text').get()

        item = BooksScraperItem()
        item['category'] = category_name
        item['name'] = book_name.strip() if book_name else ""
        item['description'] = book_description.strip() if book_description else ""
        item['upc'] = book_upc.strip() if book_upc else ""
        item['price_tax_exc'] = book_price_excl_tax.strip() if book_price_excl_tax else ""
        item['price_tax_inc'] = book_price_incl_tax.strip() if book_price_incl_tax else ""
        item['availability'] = book_availability.strip() if book_availability else ""
        item['reviews'] = book_reviews.strip() if book_reviews else ""

        yield item
