import scrapy
from scrapy_selenium import SeleniumRequest
from time import sleep
from selenium.webdriver.common.keys import Keys
import logging
from scrapy.selector import Selector
from ec_scraping.items import AmazonItem
from scrapy.loader import ItemLoader

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["www.amazon.co.jp"]
    start_urls = ["https://www.amazon.co.jp/s?rh=n%3A525592%2Cp_72%3A4-&content-id=amzn1.sym.409daf25-dd2d-47ad-a755-c771b912c06a&pd_rd_r=267eb4ea-8619-4e6e-b8e1-1b0439b5520d&pd_rd_w=AW8Rr&pd_rd_wg=Gd2xC&pf_rd_p=409daf25-dd2d-47ad-a755-c771b912c06a&pf_rd_r=2QQDJ4HC35MA9HN6J5Y0&ref=Oct_d_otopr_S"]

    # Selenium を使った詳細ページの繰り返し取得はやり方がわからなかったのでいったん保留にする
    # def start_requests(self):
    #     print('▼ start_requests ▼')
    #     yield SeleniumRequest(
    #         url = 'https://www.amazon.co.jp/s?rh=n%3A525592%2Cp_72%3A4-&content-id=amzn1.sym.409daf25-dd2d-47ad-a755-c771b912c06a&pd_rd_r=267eb4ea-8619-4e6e-b8e1-1b0439b5520d&pd_rd_w=AW8Rr&pd_rd_wg=Gd2xC&pf_rd_p=409daf25-dd2d-47ad-a755-c771b912c06a&pf_rd_r=2QQDJ4HC35MA9HN6J5Y0&ref=Oct_d_otopr_S',
    #         wait_time = 3,
    #         callback = self.parse
    #     )

    def parse(self, response):
        print('▼ parse ▼')

        logging.info(response.url)
        # driver = response.meta['driver']

        for url in response.xpath('//div[@class="sg-row"]//h2/a/@href'):
            yield response.follow(url=url, callback=self.parse_detail)

        # バージョン5
        # yield SeleniumRequest(
        #     url = response.urljoin(response.xpath('//div[@class="sg-row"]//h2/a/@href').get()),
        #     wait_time = 3,
        #     callback = self.parse_detail
        # )

        # バージョン4　→　parse_detail は呼び出されるが「driver = response.meta['driver'] \n KeyError: 'driver'」となる
        # yield response.follow(url=response.xpath('//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]/a/@href').get(), callback=self.parse_detail)

        # バージョン3
        # loader = ItemLoader(item=AmazonItem(), response=response)
        # loader.add_xpath('title', '//div[@class="sg-row"]//h2//span/text()')
        # yield loader.load_item()

        # バージョン2
        # for book in response.xpath('//div[@class="sg-row"]'):
        #     yield {
        #         'title': book.xpath('.//h2//span').get()
        #     }

        # バージョン1
        # yield {
        #     'title': response.xpath('//div[@class="sg-row"]//h2//span/text()').get()
        # }

    # 詳細ページからの情報取得
    def parse_detail(self, response):
        print('▼ parse_detail ▼')

        logging.info(response.url)
        # driver = response.meta['driver']

        yield {
            '◆ title': response.xpath('//span[@id="productTitle"]/text()').get(),
            '◆ date': response.xpath('//span[@id="productSubtitle"]/text()').get()            
        }