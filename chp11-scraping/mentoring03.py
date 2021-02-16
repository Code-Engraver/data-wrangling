# 페이지에서 보여지는 제목과 설명, 해당 링크를 크롤링 한다.
# 2021년 2월 16일 기준으로 책의 사이트와 상이하기 때문에 새로운 코드를 이용한다.

from bs4 import BeautifulSoup
import requests

page = requests.get('https://enoughproject.org/get-involved/take-action')

bs = BeautifulSoup(page.content, 'html.parser')

# 해당 내용이 들어있는 main dom을 먼저 선택한다.
# 사이트 내에서 클래스 이름을 이곳저곳에 혼용했기 때문에 처음부터 리스트 단위로 접근하는 것은 어렵다.
target_content = bs.select_one(
    '#post-11164 > div > div:nth-child(3) > div.wpb_column.vc_column_container.vc_col-sm-9 > div > div'
)

title_div_list = target_content.select('h6')
# 첫 번째 wpb_wrapper 클래스는 전체 설명을 나타낸다.
content_div_list = target_content.select('.wpb_wrapper')[1:]

all_data = []
for title_div, content_div in zip(title_div_list, content_div_list):
    data_dict = dict()
    data_dict['title'] = title_div.text.strip()
    about_p, link_p = content_div.select('p')
    data_dict['about'] = about_p.text.strip()
    data_dict['link'] = link_p.a.get('href')
    all_data.append(data_dict)

print(all_data)
