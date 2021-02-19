from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
browser.get('http://google.com')

inputs = browser.find_elements_by_css_selector('form input')
for i in inputs:
    if i.is_displayed():
        search_bar = i
        break

search_bar.send_keys('web scraping with python')
# 검색 버튼을 찾는 것보다 엔터로 해결
search_bar.send_keys(Keys.RETURN)

browser.implicitly_wait(10)
results = browser.find_elements_by_css_selector('div h3')

for r in results:
    action = webdriver.ActionChains(browser)
    action.move_to_element(r).perform()
    # 브라우저 화면의 스크롤이 필요하다.
    browser.execute_script("arguments[0].scrollIntoView();", r)
    sleep(2)

browser.quit()
