class BooksScraperPipeline:
    def process_item(self, item, spider):
        with open("books_details.xlsx", "a", encoding="utf-8") as excel_file:
            if excel_file.tell() == 0:
                header = "category\tname\tdescription\tupc\tprice_tax_inc\tprice_tax_exc\tavailability\treviews\n"
                excel_file.write(header)

            row = "\t".join([item['category'], item['name'], item['description'], item['upc'], item['price_tax_inc'], item['price_tax_exc'], item['availability'], item['reviews']])
            excel_file.write(f"{row}\n")
