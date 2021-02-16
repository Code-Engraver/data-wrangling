# 저작권과 등록상표 같은 미디어법에 익숙해지면 타인의 지적재산이라 여겨질 수 있는 데이터를 수집할 때
# 수집 범위나 방법을 결정하기가 쉬워진다.
# 수집하고자 하는 분야에서 허용되거나 불허된 사레들, 또는 법적으로 고지된 내용들에 대해 알아보고
# 각 사이트에 존재하는 robots 파일을 정독하여 사이트 소유자의 정책을 파악하도록 하자.
# 특정 사이트의 데이터 수집 가능 여부가 궁금할 때에는 변호사나 사이트에 직접 문의하는 것이 좋다.
# 본인이 사는 지역이나 사용 목적에 따라 관련 디지털 미디어 법무 기관에 수집하고자 하는 데이터와 사용하고자 하는 목적을 알리고
# 법규와 판례에 대해 물어보는 것도 좋은 방법이다.

# 파이썬 2에서 존재하면 urllib2 는 사라졌다.
# 해당 메서드들을 대체하는 파이썬 3 메서드를 사용했다.
import urllib.request
import urllib.parse
import requests

google = urllib.request.urlopen('http://google.com')

google = google.read()

print(google[:200])

url = 'http://google.com?q='
url_with_query = url + urllib.parse.quote_plus('python web scraping')

web_search = urllib.request.urlopen(url_with_query)
web_search = web_search.read()

print(web_search[:200])

google = requests.get('http://google.com')
print(google.status_code)
print(google.content[:200])
print(google.headers)
print(google.cookies.items())
