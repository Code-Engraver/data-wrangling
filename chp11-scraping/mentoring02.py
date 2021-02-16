from bs4 import BeautifulSoup
import requests

page = requests.get('https://enoughproject.org/get-involved/take-action')

bs = BeautifulSoup(page.content, 'html.parser')

# print('제목')
# print(bs.title)
# print('=' * 100)

# print('a 태그 목록')
# print(bs.find_all('a'))
# print('=' * 100)

# print('p 태그 목록')
# print(bs.find_all('p'))
# print('=' * 100)

header_children = [c for c in bs.head.children]

# head 태그 안의 자식 태그
# print('head 태그 안의 자식 태그')
# print(header_children)
# print('=' * 100)

# 2021년 2월 16일 기준으로 primary-menu 를 이용해야
# 네비게이션 목록과 그 하단의 자식들을 출력할 수 있다.
navigation_bar = bs.find(id='primary-menu')

for d in navigation_bar.descendants:
    print(d)
    if d.previous_sibling:
        for s in d.previous_sibling:
            print(s)
    print('=' * 100)

