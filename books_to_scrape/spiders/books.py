import scrapy

class BooksSpider(scrapy.Spider):
    name = "books_spider"
    start_urls = ["https://books.toscrape.com/index.html"]

    def parse(self, response):
        books_urls = response.css(".product_pod h3 a::attr(href)").getall()
        yield from response.follow_all(books_urls, callback=self.parse_details)
        next_page = response.css(".next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_details(self, response):
        flag = response.css(".icon-ok").get()
        in_stock = True if flag else False
        yield {
            "url" : response.url,
            "name": response.css(".product_main h1::text").get(),
            "category" : response.css(".breadcrumb a::text ").getall()[-1],
            "price" :  float(response.css(".product_main h1 + p::text").get().replace("£", "")),
            "description" : response.css(".sub-header + p::text").get(),
            "imageUrl": response.css(".item.active img::attr(src)").get(),
            "inStock": in_stock,
            "productInfo": self.extract_products_info(response.css(".table.table-striped tr")),
            "productsAvailble": int(response.css(".instock.availability ::text").re_first("\d+"))
        }

    def extract_products_info(self, value):
        products_info = {}
        for item in value:
            heading = item.css("th::text").get()
            val = item.css("td::text").get()
            products_info[heading] = val
        return products_info




