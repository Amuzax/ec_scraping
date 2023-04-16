# 【市場調査】Amazon/ヤフオクの市場の調査をお願いします。初心者歓迎/隙間時間にもできます
# https://crowdworks.jp/public/jobs/9151993

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# ヤフオクは robot.txt で拒否される
# 2023-04-04 02:29:07 [scrapy.downloadermiddlewares.robotstxt] DEBUG: Forbidden by robots.txt: <GET https://auctions.yahoo.co.jp/category/list/2084032133/?nockie=1&s1=featured&o1=d>

class YafuokuSpider(CrawlSpider):
    name = "yafuoku_crawl"
    allowed_domains = ["auctions.yahoo.co.jp"]
    start_urls = [
        # 過去180日間に落札された「輸入品」の商品
        # "https://auctions.yahoo.co.jp/closedsearch/closedsearch?p=+%28%E8%BC%B8%E5%85%A5%E5%93%81%29&vo=%E8%BC%B8%E5%85%A5%E5%93%81&aucminprice=2000&aucmaxprice=10000&istatus=1&abatch=2&b=1&n=20&select=3",
        # 過去180日間に落札された「ゴルフ ウェア」の商品
        # "https://auctions.yahoo.co.jp/closedsearch/closedsearch?p=%E3%82%B4%E3%83%AB%E3%83%95+%E3%82%A6%E3%82%A7%E3%82%A2&auccat=24698&va=%E3%82%B4%E3%83%AB%E3%83%95+%E3%82%A6%E3%82%A7%E3%82%A2&aucminprice=3000&aucmaxprice=10000&b=1&n=20&select=3",
        # 過去180日間に落札されたiPhone ケース -1円スタート -1円〜の商品　5,260件　落札価格 最安 3,000円 最高 10,000円 平均 4,408円
        'https://auctions.yahoo.co.jp/closedsearch/closedsearch?p=iPhone+%E3%82%B1%E3%83%BC%E3%82%B9+-1%E5%86%86%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%88+-1%E5%86%86%E3%80%9C&va=iPhone+%E3%82%B1%E3%83%BC%E3%82%B9&ve=1%E5%86%86%E3%82%B9%E3%82%BF%E3%83%BC%E3%83%88+1%E5%86%86%E3%80%9C&aucminprice=3000&aucmaxprice=10000&pstagefree=1&b=1&n=20&select=2',
    ]

    rules = (
        # 詳細ページへのリンク
        Rule(LinkExtractor(restrict_xpaths='//a[@class="Product__titleLink"]'), callback="parse_item", follow=False),
        # 次のページへのリンク
        # Rule(LinkExtractor(restrict_xpaths='//a[@data-cl-params="_cl_vmodule:pagination;_cl_link:next;_cl_position:1;"]')),
    )

    def get_name(self, elem):
        if elem:
            return elem.replace('　', '')
    
    def get_price(self, elem):
        if elem:
            return int(elem.split()[0].replace(',', '').replace('円', ''))
        return 0
    
    def get_bid_num(self, elem):
        if elem:
            return int(elem.replace('件', ''))
        return 0
    
    def get_seller(self, elem):
        if elem:
            return elem.strip()
        return elem
    
    def get_seller_rating(self, elem):
        if elem:
            return elem[0].strip().replace(',', '')
        return 0
    
    def parse_item(self, response):
        print('▼ parse_item ▼')
        yield {
            'name': self.get_name(response.xpath('(//h1/text())[1]').get()),
            'price': self.get_price(response.xpath('(//dd[@class="Price__value"]/text())[1]').get()),
            'bid_num': self.get_bid_num(response.xpath('//span[contains(@class,"Count__detail") and contains(text(),"件")]/text()').get()),
            'postage': response.xpath('//span[@class="Price__postageValue Price__postageValue--free"]/text()').get(),
            'free_postage': response.xpath('(//span[@title="送料無料"]/text())[1]').get(),
            'unused': response.xpath('(//span[@title="未使用"]/text())[1]').get(),
            'seller': self.get_seller(response.xpath('//p[@class="Seller__name"]/a/text()').get()),
            'seller_rating': self.get_seller_rating(response.xpath('//a[@class="Seller__ratingLink"]/text()').getall()),
            'url': response.url
        }
