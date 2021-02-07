"""
잡음이 많은 데이터세트에서 중복 기록을 찾기 위해 사용할 수 있는 퍼지 매칭

두 개 이상의 데이터 세트를 사용하고 있거나 깔끔하지 않고 통일성이 없는 데이터를 사용하고 있다면
퍼지 매칭을 활용하여 중복 기록을 찾아 결합할 수 있다.
퍼지 매칭을 사용하면 두 항목(보통 문자열) 이 '동일한지' 판단할 수 있다.
자연어 처리나 머신 러닝처럼 심도 있는 방법은 아니지만 퍼지 매칭을 이용하면
'My dog & I' 와 'me and my dog' 의 두 항목이 비슷한 의미를 가졌다고 연결 지을 수 있다.

경고창이 출력되는 경우 python-Levenshtein 을 추가로 설치해주면 해결 된다.
"""
from fuzzywuzzy import fuzz, process

my_records = [
    {
        'favorite_book': 'Grapes of Wrath',
        'favorite_movie': 'Free Willie',
        'favorite_show': 'Two Broke Girls'
    },
    {
        'favorite_book': 'The Grapes of Wrath',
        'favorite_movie': 'Free Willy',
        'favorite_show': '2 Broke Girls'
    }
]

print(fuzz.ratio(my_records[0].get('favorite_book'), my_records[1].get('favorite_book')))
print(fuzz.ratio(my_records[0].get('favorite_movie'), my_records[1].get('favorite_movie')))
print(fuzz.ratio(my_records[0].get('favorite_show'), my_records[1].get('favorite_show')))

print()

# partial_ratio 함수를 이용하면 서브 문자열을 비교할 수 있기 때문에 특정 단어를 빠뜨리거나 철자 오류가 있다해도 큰 문제가 되지 않는다.
print(fuzz.partial_ratio(my_records[0].get('favorite_book'), my_records[1].get('favorite_book')))
print(fuzz.partial_ratio(my_records[0].get('favorite_movie'), my_records[1].get('favorite_movie')))
print(fuzz.partial_ratio(my_records[0].get('favorite_show'), my_records[1].get('favorite_show')))

print()

# 데이터에 존재하는 비 일관성이 복잡하지 않다면 몇 가지 훌륭한 함수를 이용해 제대로 매칭되지 않은 부분을 찾아낼 수 있다.
# 그러나 몇 글자 차이로 의미가 크게 달라진다면 유사도와 차이를 테스트해 보아야 한다.
# 예를 들어 does 와 doesn't 이 두 단어는 의미를 완전히 다르지만 철자에 있어서는 크게 다르지 않다.
# 즉, 데이터에 대한 이해가 되어 있는 상태에서 적절하게 사용해야 한다.

my_records = [
    {
        'favorite_food': 'cheeseburgers with bacon',
        'favorite_drink': 'wine, beer, and tequila',
        'favorite_dessert': 'cheese or cake'
    },
    {
        'favorite_food': 'burgers with cheese and bacon',
        'favorite_drink': 'beer, wine, and tequila',
        'favorite_dessert': 'cheese cake'
    }
]

# I like dogs and cats 와 I like cats and dogs 처럼 같은 의미를 갖지만 순서가 다른 경우를 판별할 수 있다.
print(fuzz.token_sort_ratio(my_records[0].get('favorite_food'), my_records[1].get('favorite_food')))
print(fuzz.token_sort_ratio(my_records[0].get('favorite_drink'), my_records[1].get('favorite_drink')))
print(fuzz.token_sort_ratio(my_records[0].get('favorite_dessert'), my_records[1].get('favorite_dessert')))

print()

# 토큰의 set을 비교하여 교집합과 차집합을 확인한다.
# token_sort_ratio 와 token_set_ratio 의 결과를 보면 cheese or cake 와 cheese cake는 다른 의미 이지만 긍정 로규가 발생한다.
# 또한 cheeseburger를 의미한 단어들에는 반응하지 못한다.
print(fuzz.token_set_ratio(my_records[0].get('favorite_food'), my_records[1].get('favorite_food')))
print(fuzz.token_set_ratio(my_records[0].get('favorite_drink'), my_records[1].get('favorite_drink')))
print(fuzz.token_set_ratio(my_records[0].get('favorite_dessert'), my_records[1].get('favorite_dessert')))

print()

# 같은 의미를 가지고 있는 단어를 뽑아낼 수 있다.
choices = ['Yes', 'No', 'Maybe', 'N/A']
print(process.extract('ya', choices, limit=2))
print(process.extractOne('ya', choices))
print(process.extract('nope', choices, limit=2))
print(process.extractOne('nope', choices))
