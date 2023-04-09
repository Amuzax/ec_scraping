import scrapy
from scrapy_selenium import SeleniumRequest
from time import sleep
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector

class AmazonAsinSearchSpider(scrapy.Spider):
    name = "amazon_asin_search"

    def start_requests(self):
        print('▼ start_requests ▼')
        yield SeleniumRequest(
            url = 'https://www.amazon.co.jp/',
            wait_time = 3,
            screenshot = False,
            callback = self.parse
        )

    # def strip_elem(self, elem):
    #     if elem:
    #         return elem.strip()
    #     return '-'
    
    # def get_asin(self, elem):
    #     if elem:
    #         return elem.replace('‎', '').strip()
    #     return '-'
    
    # def get_min(self, elem):
    #     if elem:
    #         return int(elem.replace(' この商品の最小注文個数は', '').replace('です ', ''))
    #     return 1

    def parse(self, response):
        print('▼ parse ▼')
        driver = response.meta['driver']

        ASIN = 'B001VZNABO'

        search_text = driver.find_element_by_xpath('//input[@id="twotabsearchtextbox"]')
        search_text.send_keys(ASIN)
        search_button = driver.find_element_by_xpath('//input[@id="nav-search-submit-text"]')
        search_button.submit()
        sleep(3)

        w = driver.execute_script('return document.body.scrollWidth')
        h = driver.execute_script('return document.body.scrollHeight')
        driver.set_window_size(w, h)
        driver.save_screenshot('amazon.png')

        # html = driver.page_source
        # selector = Selector(text=html)

        # yield{
        #     # 商品名
        #     # 'name': response.xpath('//span[@id="productTitle"]/text()').get(),
        #     'name': self.strip_elem(response.xpath('//span[@id="productTitle"]/text()').get()),
        #     # 'asin_1': response.xpath('//span[contains(text(),"ASIN")]/following-sibling::span/text()').get(),
        #     'asin_1': self.strip_elem(response.xpath('//span[contains(text(),"ASIN")]/following-sibling::span/text()').get()),
        #     # 'asin_2': response.xpath('//th[contains(text(), "ASIN")]/following-sibling::td/text()').get(),
        #     'asin_2': self.get_asin(response.xpath('//th[contains(text(), "ASIN")]/following-sibling::td/text()').get()),
        #     # 最小注文個数
        #     # 'min_order': response.xpath('//a[@id="trigger_popover"]/text()').get(),
        #     'min_order': self.get_min_order(response.xpath('//a[@id="trigger_popover"]/text()').get()),
        #     # 'price': response.xpath('(//div[@id="corePriceDisplay_desktop_feature_div"]//span[@class="a-price-whole"])[1]').get(),
        #     'url': response.url,
        # }