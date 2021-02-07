"""
정규식 매칭
문자열 패턴이나 데이터 패턴을 매칭하고 찾아 내고 제거하게 할 수 있다.
"""
import re

word = r'\w+'
sentence = 'Here is my sentence.'

# 모든 매칭 결과를 담은 리스트를 반환
print(re.findall(word, sentence))

# 매칭되는 첫 번째 결과 반환
search_result = re.search(word, sentence)
print(search_result.group())

# 매칭되는 첫 번째 결과 반환
match_result = re.match(word, sentence)
print(match_result.group())
print(match_result.group(0))

print()

# match는 문자열의 가장 첫 부분을 검사한다.
# search는 문자열에서 매칭되는 부분을 찾을 때 까지 검사한다.
number = r'\d+'
capitalized_word = r'[A-Z]\w+'

sentence = 'I have 2 pets: Bear and Bunny.'

search_number = re.search(number, sentence)
print(search_number.group())

match_number = re.match(number, sentence)
print(match_number)

search_capital = re.search(capitalized_word, sentence)
print(search_capital.group())

match_capital = re.match(capitalized_word, sentence)
print(match_capital)

print()

name_regex = r'([A-Z]\w+) ([A-Z]\w+)'

names = 'Barack Obama, Ronald Reagan, Nancy Drew'

name_match = re.match(name_regex, names)
print(name_match.group())
print(name_match.groups())

# ?P<변수명> 을 이용하여 패턴 그룹을 명명하면 코드를 이해하는 데 도움이 된다.
name_regex = r'(?P<first_name>[A-Z]\w+) (?P<last_name>[A-Z]\w+)'

# finditer는 findall 과 비슷하지만 반복자를 반환한다.
for name in re.finditer(name_regex, names):
    print(f'Meet {name.group("first_name")}')
