# 자바스크립트를 많이 사용하여 페이지 로드가 끝난 이후 콘텐츠를 채우는 페이지는
# 통상적으로 사용하는 웹 스크래퍼를 사용할 수 없다.
# 이런 경우에는 스크린 리딩이 필요하다.
# 가장 흔히 쓰이는 스크린 리딩 라이브러리는 셀레니움이다.
# 셀레니움은 기본적으로 firefox 드라이버가 내장되어 있다.
# 다른 브라우저를 사용하기 위해서는 알맞은 드라이버를 설치해야 한다.
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import json

browser = webdriver.Firefox()
browser.get('http://www.fairphone.com/en/community/')

browser.maximize_window()

# 책의 예제는 2016년 자료라 동작하지 않는다.
# 2021년 2월 18일 기준으로 위 링크로 접근시 나오는 'Our Ambassadors' 를 가져오도록 하자
# 11명의 사람이 나올 것이고 클릭하면 각자의 정보를 알 수 있을 것이다.
# 디테일 구조를 보면 사진/이름/소개 까지는 같으나 하단의 소셜 링크는 다른 것을 알 수 있다.
# 크롤링 코드를 생각해내는 흐름을 파악하는 것을 위해 추상화 작업은 하지않고, raw한 상태를 유지하였다.

# 먼저 ul 태그를 선택하여 가져오도록 하자.
# 하나의 ul을 가져올 예정이므로 full xpath를 통해 지목한다.
ul_element = browser.find_element_by_xpath('/html/body/section[2]/div/div/div/div/div/ul')

# HTML을 출력해보면 사실상 모든 데이터가 존재한다.
# 이런 경우에는 스크린리더를 사용하는 것보다 스크래퍼를 사용하는게 효율적이다.
# print(ul_element.get_attribute('innerHTML'))

# 구조적으로 ul을 탐색해본 결과 가장 쉽게 가는 것은 li를 추출하는 것이 아니라 div를 추출하는 것이다.
# li 태그 밑에 팝업을 위해 만들어 놓은 div 에 모든 정보가 들어있다.
# c-ambassadors__popup 라는 클래스를 지닌 div를 ul_element에서 추출한다.
detail_popup_list = ul_element.find_elements_by_class_name('c-ambassadors__popup')
# 11개가 출력되는 것을 보니 제대로 따온 듯 하다.
# print(len(detail_popup_list))

result_list = list()
# 클래스에 각각의 기능을 잘 명시해두었다. 클래스를 기준으로 데이터를 추출하도록 한다.
for detail_popup in detail_popup_list:
    result_dict = dict()
    # 이미지의 링크는 data-src 라는 곳에 존재한다.
    img_element = detail_popup.find_element_by_class_name('c-ambassadors__popup-image').find_element_by_tag_name('img')
    profile_image_link = img_element.get_attribute('data-src')
    result_dict['profile_image_link'] = profile_image_link

    # get_attribute('textContent')를 이용하면 내부 문자열을 얻을 수 있다.
    title = detail_popup.find_element_by_class_name('c-ambassadors__popup-title').get_attribute('textContent').strip()
    result_dict['title'] = title

    # 지역은 있는 경우도 있고 없는 경우도 있다.
    # 없을 때 NoSuchElementException 오류가 발생한다.
    try:
        location_element = detail_popup.find_element_by_class_name('c-ambassadors__popup-location')
    except NoSuchElementException:
        location_element = None
    location = location_element.get_attribute('textContent').strip() if location_element else ""
    result_dict['location'] = location

    # c-ambassadors__popup-bio 클래스를 선택하면
    # p 태그에는 설명이 적혀있고, bullet 클래스에는 소셜 정보가 들어있다.
    # 하지만 조금 더 자세히 보면 규칙성이 깨져 있는 것을 알 수 있다.
    # bullet 클래스 안에 li를 넣은 경우 / li 만 있는 경우 / p 만 사용한 경우 가 있다는 것을 알 수 있다.
    bio_element = detail_popup.find_element_by_class_name('c-ambassadors__popup-bio')

    # 소셜 부분을 기준으로 계층을 나누어 정제하도록 하자.
    # 1. .bullet 이 있는 경우 => 없다면 예외 발생
    # 2. li 를 가지고 있는 경우 => 없다면 예외 발생 (p: about, li: 소설)
    # 3. p 만 가지고 있는 경우 => ':' 를 이용하여 구분
    social_info_list = list()
    try:
        social_li_list = bio_element.find_element_by_class_name('bullet').find_elements_by_tag_name('li')

        for social_li in social_li_list:
            social_a_list = social_li.find_elements_by_tag_name('a')
            social_href_list = [tag.get_attribute('href') for tag in social_a_list]

            social_li_text = social_li.get_attribute('textContent')
            social_li_text = social_li_text.replace('http:', '').replace('https:', '')

            if len(social_li_text.split(':')) != 2:
                print(social_li_text)
                raise Exception

            social_title = social_li_text.split(':')[0]
            social_title = ' '.join([word.strip() for word in social_title.split(' ') if len(word.strip()) != 0]).strip()

            social_dict = {social_title: social_href_list}
            social_info_list.append(social_dict)

        result_dict['social_info_list'] = social_info_list

        about = bio_element.find_elements_by_tag_name('p')
        about = ' '.join([tag.get_attribute('textContent') for tag in about])
        about = ' '.join([word.strip() for word in about.split(' ') if len(word.strip()) != 0]).strip()
        result_dict['about'] = about
    except NoSuchElementException:
        try:
            social_li_list = bio_element.find_elements_by_tag_name('li')
            if not social_li_list:
                raise NoSuchElementException

            for social_li in social_li_list:
                social_a_list = social_li.find_elements_by_tag_name('a')
                social_href_list = [tag.get_attribute('href') for tag in social_a_list]

                social_li_text = social_li.get_attribute('textContent')
                social_li_text = social_li_text.replace('http:', '').replace('https:', '')

                if len(social_li_text.split(':')) != 2:
                    raise Exception

                social_title = social_li_text.split(':')[0]
                social_title = ' '.join([word.strip() for word in social_title.split(' ') if len(word.strip()) != 0]).strip()

                social_dict = {social_title: social_href_list}
                social_info_list.append(social_dict)

            result_dict['social_info_list'] = social_info_list

            about = bio_element.find_elements_by_tag_name('p')
            about = ' '.join([tag.get_attribute('textContent') for tag in about])
            about = ' '.join([word.strip() for word in about.split(' ') if len(word.strip()) != 0]).strip()
            result_dict['about'] = about

        except NoSuchElementException:
            p_list = bio_element.find_elements_by_tag_name('p')

            about = p_list[0].get_attribute('textContent')
            about = ' '.join([word.strip() for word in about.split(' ') if len(word.strip()) != 0]).strip()
            result_dict['about'] = about

            social_li_list = p_list[1:]
            for social_li in social_li_list:
                social_li_text = social_li.get_attribute('textContent').replace('http:', '').replace('https:', '')
                social_li_text_list = social_li_text.split(' ')
                social_title_list = [text.strip().replace(':', '') for text in social_li_text_list if ':' in text]

                social_a_list = social_li.find_elements_by_tag_name('a')
                social_href_list = [tag.get_attribute('href') for tag in social_a_list]

                if len(social_title_list) != len(social_href_list):
                    raise Exception

                for title, href in zip(social_title_list, social_href_list):
                    social_dict = {title: [href]}
                    social_info_list.append(social_dict)

            result_dict['social_info_list'] = social_info_list

    result_list.append(result_dict)

print(json.dumps(result_list, indent=4, ensure_ascii=False))

browser.close()
