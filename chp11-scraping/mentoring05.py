# 이모티콘 리스트를 불러오는 코드이다.
# 2021년 2월 16일 기준으로 책의 코드와 상이하므로 새로운 코드를 제시한다.
from lxml import html
import requests

resp = requests.get('https://www.webfx.com/tools/emoji-cheat-sheet/')
page = html.document_fromstring(resp.content)

title_list = page.cssselect('h2')

# 마지막을 제외해야 한다는 것을 알 수 있다.
# for title in title_list:
#     print(html.tostring(title))
#     print()

title_list = title_list[:len(title_list) - 1]

# id를 보면 emoji-[h2.lower()] 의 형태임을 알 수 있다.
title_list = [title.text_content().strip().lower() for title in title_list]

# key: header / value: htmlelement 객체 리스트
result_dict = dict()
for title in title_list:
    emoji_ul_id = f'emoji-{title}'

    emoji_ul = page.cssselect(f'#{emoji_ul_id}')[0]

    emoji_li_list = emoji_ul.cssselect('li')

    result_dict[title] = emoji_li_list

print(result_dict)
