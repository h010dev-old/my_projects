import scrapy


class SofifaSpider(scrapy.Spider):

    name = 'sofifa'

    def start_requests(self):

        urls = [
            'https://sofifa.com/players'
        ]

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):

        for row in response.selector.xpath("//table[@class='table table-hover persist-area']/tbody/tr"):
            yield {
                # 'id': row.xpath(".//tbody//figure[@class='avatar']//img[contains(@id, '')]").extract_first(),
                'name': row.xpath(".//a[contains(@href, '/player/')]/text()[1]").extract_first(),
                'position': row.xpath(".//span[contains(@class, 'pos')]/text()[1]").extract(),
                'age': row.xpath(".//*[@class='col-digit col-ae']/text()[1]").extract_first(),
                'overall': row.xpath(".//*[@class='col-digit col-oa']/span/text()[1]").extract_first(),
                'potential': row.xpath(".//*[@class='col-digit col-pt']/span/text()[1]").extract_first(),
                'team': row.xpath(".//a[contains(@href, '/team/')]/text()[1]").extract_first(),
                'contract': row.xpath(".//div[@class='subtitle text-ellipsis rtl']/text()[1]").extract_first(),
                'value': row.xpath(".//div[@class='col-digit col-vl']/text()[1]").extract_first(),
                'wage': row.xpath(".//div[@class='col-digit col-wg']/text()[1]").extract_first(),
                'total_stats': row.xpath(".//div[@class='col-digit col-tt']/text()[1]").extract_first(),
                'hits_comments': row.xpath(".//div[@class='col-comments text-right text-ellipsis rtl']"
                                           "/text()[1]").extract_first()
            }

        second_page = response.selector.xpath(f"//a[@class='btn pjax'][{1}]/@href").extract_first()
        next_page = response.selector.xpath(f"//a[@class='btn pjax'][{2}]/@href").extract_first()

        if next_page is None:
            # Used for first page only, since there is no previous button
            second_page_link = response.urljoin(second_page)
            yield scrapy.Request(url=second_page_link, callback=self.parse)

        elif next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)