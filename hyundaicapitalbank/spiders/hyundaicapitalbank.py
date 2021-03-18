import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from hyundaicapitalbank.items import Article


class HyundaicapitalbankSpider(scrapy.Spider):
    name = 'hyundaicapitalbank'
    start_urls = ['https://www.hyundaicapitalbank.eu/presse/']

    def parse(self, response):
        titles = response.xpath('//div[@id="accordion"]/h3/text()[2]').getall()
        dates = response.xpath('//div[@id="accordion"]/h3/span/text()').getall()
        contents = response.xpath('//div[@id="accordion"]/div/div[contains(@class, "entry-content")]')
        contents = [content.xpath('.//text()').getall() for content in contents]

        for i in range(len(titles)):
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = titles[i]
            date = dates[i]
            content = contents[i]
            content = [text for text in content if text.strip()]
            content = "\n".join(content).strip()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()
