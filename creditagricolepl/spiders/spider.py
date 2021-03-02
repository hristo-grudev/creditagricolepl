import scrapy

from scrapy.loader import ItemLoader
from ..items import CreditagricoleplItem
from itemloaders.processors import TakeFirst


class CreditagricoleplSpider(scrapy.Spider):
	name = 'creditagricolepl'
	start_urls = ['https://www.credit-agricole.pl/o-banku/aktualnosci']

	def parse(self, response):
		post_links = response.xpath('//li[@class="search-results__item"]/article/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="article-navigation__item article-navigation__item--previous"]/a[@class="article-navigation__link"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//article[@class="simple-article"]/h1/text()').get()
		description = response.xpath('//div[@class="wyswig"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=CreditagricoleplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
