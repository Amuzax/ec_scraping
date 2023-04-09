import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AmazonCrawlSpider(CrawlSpider):
    name = "amazon_crawl"
    allowed_domains = ["www.amazon.co.jp"]

    '''
    # クラウドワークス：【市場調査】Amazon/ヤフオクの市場の調査をお願いします。初心者歓迎/隙間時間にもできます
    # https://crowdworks.jp/public/jobs/9151993

    start_urls = ["https://www.amazon.co.jp/gp/bestsellers/computers/ref=zg_bs_nav_0"]  # (1)
    # ↑　取れない。リダイレクトされているから？
    # →　そうだった。settings.py に MEDIA_ALLOW_REDIRECTS = True を指定すれば取れるようになった。
    # 参考）https://doc-ja-scrapy.readthedocs.io/ja/latest/topics/media-pipeline.html#std:setting-MEDIA_ALLOW_REDIRECTS

    start_urls = ["https://www.amazon.co.jp/s?rh=n%3A525592%2Cp_72%3A4-&content-id=amzn1.sym.409daf25-dd2d-47ad-a755-c771b912c06a&pd_rd_r=267eb4ea-8619-4e6e-b8e1-1b0439b5520d&pd_rd_w=AW8Rr&pd_rd_wg=Gd2xC&pf_rd_p=409daf25-dd2d-47ad-a755-c771b912c06a&pf_rd_r=2QQDJ4HC35MA9HN6J5Y0&ref=Oct_d_otopr_S"]  # (2)
    # ↑　取れない。詳細ページが別ウインドウで開かれる（target="_blank"）から？
    # 2023-04-04 02:41:44 [scrapy.downloadermiddlewares.redirect] DEBUG: Redirecting (301) to <GET https://www.amazon.co.jp/Anker-PowerLine-%E3%83%A9%E3%82%A4%E3%83%88%E3%83%8B%E3%83%B3%E3%82%B0USB%E3%82%B1%E3%83%BC%E3%83%96%E3%83%AB%E3%80%90Apple-%E8%B6%85%E9%AB%98%E8%80%90%E4%B9%85%E3%80%91iPhone-iPod%E5%90%84%E7%A8%AE%E5%AF%BE%E5%BF%9C/dp/B01N40PO2M> from <GET https://www.amazon.co.jp/Anker-PowerLine-%E3%83%A9%E3%82%A4%E3%83%88%E3%83%8B%E3%83%B3%E3%82%B0USB%E3%82%B1%E3%83%BC%E3%83%96%E3%83%AB%E3%80%90Apple-%E8%B6%85%E9%AB%98%E8%80%90%E4%B9%85%E3%80%91iPhone-iPod%E5%90%84%E7%A8%AE%E5%AF%BE%E5%BF%9C/dp/B01N40PO2M/ref=zg_bs_computers_sccl_1/000-0000000-0000000?psc=1>

    rules = (Rule(LinkExtractor(restrict_xpaths='//div[@id="gridItemRoot"]//a[@tabindex="-1"]'), callback="parse_item", follow=False),)

    def parse_item(self, response):
        # print('▼ parse_item ▼')
        # (1)用
        yield {
            'name': response.xpath('//span[@id="productTitle"]/text()').get(),
            'price': response.xpath('//div[@id="corePrice_feature_div"]//span[@class="a-price-whole"]/text()').get(),
            'rationg': response.xpath('(//span[@id="acrPopover"]//span[@class="a-icon-alt"]/text())[1]').get(),
        }
    '''

    # クラウドワークス：Amazonのスクレイピング 指定したASINに最小注文個数制限(MOQ)があるかの判定
    # https://crowdworks.jp/proposals/new?job_offer_id=9176577

    start_urls = ["https://www.amazon.co.jp/gp/bestsellers/toys/2189278051?ref_=Oct_d_obs_S&pd_rd_w=fs3Bd&content-id=amzn1.sym.ab53e8b4-6265-4e72-a842-b106c7f4f2d3&pf_rd_p=ab53e8b4-6265-4e72-a842-b106c7f4f2d3&pf_rd_r=JBKX55HCP6PKV4SEF6Z4&pd_rd_wg=ddY7c&pd_rd_r=c87e189e-d914-488e-ba64-5a481a058c22"]

    rules = (Rule(LinkExtractor(restrict_xpaths='//div[@class="a-cardui _cDEzb_grid-cell_1uMOS expandableGrid p13n-grid-content"]//a[@tabindex="-1"]'), callback="parse_item", follow=False),)

    def strip_elem(self, elem):
        if elem:
            return elem.strip()
        return 0
    
    def get_asin(self, elem):
        if elem:
            return elem.replace('‎', '').strip()
        return '-'
    
    def get_min(self, elem):
        if elem:
            return int(elem.replace(' この商品の最小注文個数は', '').replace('です ', ''))
        return 1

    def parse_item(self, response):
        print('▼ parse_item ▼')
        yield {
            # 商品名
            # 'name': response.xpath('//span[@id="productTitle"]/text()').get(),
            'name': self.strip_elem(response.xpath('//span[@id="productTitle"]/text()').get()),
            # 'asin_1': response.xpath('//span[contains(text(),"ASIN")]/following-sibling::span/text()').get(),
            'asin_1': self.strip_elem(response.xpath('//span[contains(text(),"ASIN")]/following-sibling::span/text()').get()),
            # 'asin_2': response.xpath('//th[contains(text(), "ASIN")]/following-sibling::td/text()').get(),
            'asin_2': self.get_asin(response.xpath('//th[contains(text(), "ASIN")]/following-sibling::td/text()').get()),
            # 最小注文個数
            # 'min': response.xpath('//a[@id="trigger_popover"]/text()').get(),
            'min': self.get_min(response.xpath('//a[@id="trigger_popover"]/text()').get()),
            # 'price': response.xpath('(//div[@id="corePriceDisplay_desktop_feature_div"]//span[@class="a-price-whole"])[1]').get(),
            'url': response.url,
        }
