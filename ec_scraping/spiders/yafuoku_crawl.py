import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# ヤフオクは robot.txt で拒否される
# 2023-04-04 02:29:07 [scrapy.downloadermiddlewares.robotstxt] DEBUG: Forbidden by robots.txt: <GET https://auctions.yahoo.co.jp/category/list/2084032133/?nockie=1&s1=featured&o1=d>
class YafuokuSpider(CrawlSpider):
    name = "yafuoku_crawl"
    allowed_domains = ["auctions.yahoo.co.jp"]
    start_urls = ["https://auctions.yahoo.co.jp/closedsearch/closedsearch?p=iPhone&auccat=2084051923&va=iPhone&aucminprice=2000&aucmaxprice=5000&pstagefree=1&thumb=1&b=1&n=20"]

    rules = (
        # 詳細ページへのリンク
        Rule(LinkExtractor(restrict_xpaths='//a[@class="Product__titleLink"]'), callback="parse_item", follow=False),
        # 次のページへのリンク
        Rule(LinkExtractor(restrict_xpaths='//a[@data-cl-params="_cl_vmodule:pagination;_cl_link:next;_cl_position:1;"]')),
    )

    def get_name(self, elem):
        if elem:
            return elem.replace('　', '')
    
    def get_price(self, elem):
        if elem:
            return int(elem.split()[0].replace(',', '').replace('円', ''))
        return 0
    
    def get_seller(self, elem):
        if elem:
            return elem.split()[0]
        return elem
    
    def parse_item(self, response):
        yield {
            'name': self.get_name(response.xpath('(//h1/text())[1]').get()),
            'price': self.get_price(response.xpath('(//dd[@class="Price__value"]/text())[1]').get()),
            # 'price': response.xpath('(//dd[@class="Price__value"]/text())[1]').get(),
            'postage': response.xpath('//span[@class="Price__postageValue Price__postageValue--free"]/text()').get(),
            'free_postage': response.xpath('(//span[@title="送料無料"]/text())[1]').get(),
            'new': response.xpath('(//span[@title="未使用"]/text())[1]').get(),
            'seller': self.get_seller(response.xpath('//p[@class="Seller__name"]/a/text()').get()),
        }
