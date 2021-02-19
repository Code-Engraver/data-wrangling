# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImojiItem(scrapy.Item):
    title = scrapy.Field()
    emoji_list = scrapy.Field()
