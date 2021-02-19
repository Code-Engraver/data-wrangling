import scrapy
from bs4 import BeautifulSoup
from scrapy_project.items import ImojiItem


class EmojiSpider(scrapy.Spider):
    name = 'emoji'
    allowed_domains = ['www.webfx.com/tools/emoji-cheat-sheet']
    start_urls = ['http://www.webfx.com/tools/emoji-cheat-sheet/']

    def parse(self, response):
        title_list = response.css('h2::text').getall()
        title_list = title_list[:len(title_list) - 1]
        for title in title_list:
            title = title.strip().lower()
            emoji_ul_id = f'emoji-{title}'

            emoji_li_list = response.css(f'#{emoji_ul_id} li').getall()
            emoji_li_list = [BeautifulSoup(li_tag, 'html.parser').select_one('.emoji').attrs['data-src'] for li_tag in emoji_li_list]

            doc = ImojiItem()
            doc['title'] = title
            doc['emoji_list'] = emoji_li_list
            yield doc
