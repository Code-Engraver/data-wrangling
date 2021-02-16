# BeautifulSoup과 차이점은 문법과 페이지가 로드되는 방법이다.
# BeautifulSoup은 정규식을 이용해 문서를 긴 문자열로 보고 파싱하는 방식이고,
# lxml은 파이썬과 C 라이브러리를 사용해 페이지 구조를 인식하고 이를 객체지향적으로 탐색한다.
# lxml는 모든 태그들의 구조를 살펴보고 가장 파싱이 빠른 방법을 사용해 트리 형태로 분석하고 데이터를 etree 오브젝트 형태로 반환한다.
from lxml import html
import urllib.request

# document를 읽어보면 URL을 넘길때는 urllib 등을 사용하여 넘기도록 되어있다.
# https://lxml.de/lxmlhtml.html
page = html.parse(urllib.request.urlopen('https://enoughproject.org/get-involved/take-action'))
root = page.getroot()

# find는 DOM을 이용하여 엘리먼트 간에 이동하며, 엘리먼트 간의 계층 구조를 이용해 찾는다.
# cssselect는 마치 jQuery 처럼 CSS 선택자를 이용하여 조건에 부합하는 페이지상의 모든 엘리먼트들을 찾아준다.
# 페이지가 CSS 클래스나 ID와 같은 식별자로 잘 정리되어 있다면 cssselect가 좋은 선택일 수 있다.
# 페이지가 잘 정리되어 있지 않고, 식별자를 별로 사용하지 않는다면 엘리먼트들의 계층 구조를 이용해 찾는 것이 도움이 될 수도 있다.
# print(root.find('div'))
# print(root.find('head'))
# print(root.find('head').findall('script'))
# print(root.cssselect('div'))
# print(root.cssselect('head script'))

# BeautifulSoup을 이용하여 했던 작업을 lxml 로도 해본다.
target_content = root.cssselect(
    '#post-11164 > div > div:nth-child(3) > div.wpb_column.vc_column_container.vc_col-sm-9 > div > div'
)[0]

title_div_list = target_content.cssselect('h6')
# cssselect 구조상 BeautifulSoup 과는 다르게 전체 div에 대해서도 찾아준다.
# 첫번째는 target_content의 전체 내용이고, 두 번째는 개괄 설명이 있는 것이다.
# 확인하는 방법은 아래와 같다.
# for content_div in content_div_list:
#     print(html.tostring(content_div))
#     print('=' * 100)
content_div_list = target_content.cssselect('.wpb_wrapper')[2:]

all_data = []
for title_div, content_div in zip(title_div_list, content_div_list):
    data_dict = dict()
    data_dict['title'] = title_div.text_content().strip()
    about_p, link_p = content_div.cssselect('p')
    data_dict['about'] = about_p.text_content().strip()
    data_dict['link'] = link_p.find('a').get('href')
    all_data.append(data_dict)

print(all_data)
