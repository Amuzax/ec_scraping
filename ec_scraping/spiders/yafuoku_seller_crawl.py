# 結果は yafuoku_seller_crawl.csv として出力する

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime

class YafuokuSellerCrawlSpider(CrawlSpider):
    name = "yafuoku_seller_crawl"
    allowed_domains = ["auctions.yahoo.co.jp"]
    start_urls = [
        # セラーの出品での評価リスト
        "https://auctions.yahoo.co.jp/jp/show/rating?userID=k_h_112&role=seller",
        "https://auctions.yahoo.co.jp/jp/show/rating?userID=mlamb63401&role=seller",
    ]

    rules = (
        # 詳細ページへのリンク
        Rule(LinkExtractor(restrict_xpaths='//table[@bgcolor="#ffffff"]//a[contains(@href,"page")]'), callback="parse_item", follow=True),
        # 次のページへのリンク
        Rule(LinkExtractor(restrict_xpaths='(//a[contains(text(),"次の25件")])[1]')),
    )

    # def get_name(self, elem):
    #     if elem:
    #         return elem.replace('　', ' ')
    #     return 'No Name'
    
    def get_price(self, elem):
        if elem:
            return int(elem.split()[0].replace(',', '').replace('円', ''))
        return 0
    
    # def get_tax(self, elem):
    #     if '税込' in elem:
    #         return int(elem.replace('（税込 ', '').replace(' 円）', '').replace(',', ''))
    #     elif '税' in elem:
    #         return int(elem.replace('（税 ', '').replace(' 円）', '').replace(',', ''))
    #     return 0

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

    def get_end_date(self, elem):
        if elem:
            end_datetime = datetime.datetime.strptime(elem.strip().split('（')[0], '%Y.%m.%d')
            end_date = datetime.date(end_datetime.year, end_datetime.month, end_datetime.day)
            diff_date = datetime.date.today() - end_date
            if diff_date.days > 60:
                print(f'■ {diff_date} ■')
                raise CloseSpider('■■■ 古い情報になったため調査を終了します ■■■')
            print(f'■ {diff_date} ■')
            return end_date
        return 0

    def parse_item(self, response):
        # print('▼ parse_item ▼')
        yield {
            'name': response.xpath('//h1/text()').get(),
            'price': self.get_price(response.xpath('(//dd[@class="Price__value"]/text())[1]').get()),
            'tax': response.xpath('//span[@class="Price__tax u-fontSize14"]/text()').get(),
            # 'tax': self.get_tax(response.xpath('//span[@class="Price__tax u-fontSize14"]/text()').get()),
            'bid_num': self.get_bid_num(response.xpath('//span[contains(@class,"Count__detail") and contains(text(),"件")]/text()').get()),
            'postage': response.xpath('//span[@class="Price__postageValue Price__postageValue--free"]/text()').get(),
            'postage_due': response.xpath('(//dt[contains(text(),"送料負担")]/following-sibling::dd/text())[2]').get(),
            'free_postage': response.xpath('(//span[@title="送料無料"]/text())[1]').get(),
            'unused': response.xpath('(//span[@title="未使用"]/text())[1]').get(),
            'seller': self.get_seller(response.xpath('//p[@class="Seller__name"]/a/text()').get()),
            'seller_rating': self.get_seller_rating(response.xpath('//a[@class="Seller__ratingLink"]/text()').getall()),
            'info_get_date': datetime.datetime.now(),
            'end_date': self.get_end_date(response.xpath('//th[contains(text(),"終了日時")]/following-sibling::td/text()').get()),
            'url': response.url
        }