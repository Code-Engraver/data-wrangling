import sys

# 파이썬 라이브러리가 설치되어 있는 디렉토리 경로 출력
# 해당 경로에 추가된 경우 디렉토리로 이동할 필요 없이 바로 불러서 사용 가능
print(sys.path)

# 문자열
'cat'
'This is a string'
'5'
'walking'
'$G00barBaz340 '
"cat"

# 정수
10
1
0
-1
-10

# 정수와 문자열 차이
# 핸드폰 번호나 우편 번호 등은 숫자가 아니라 문자열이다.
# 연산에서 사용되는 숫자가 아니라면 대부분 문자열이다.
print(5 == '5')

# 책에서는 2.x 를 사용하기 때문에 안된다고 설명하지만 3.x 에서는 가능하다.
print(2/3)

# 실수는 부동소수점의 구조상 정확한 계산이 안될 수 있다.
# 그래서 계산기와 같은 정확한 작업을 수행할 때는 decimal 라이브러리를 사용해야 한다.
from decimal import getcontext, Decimal
# 소수점을 컨트롤 한다. 2로 바꿔보면 계산 결과가 소수 2번째까지 나온다.
getcontext().prec = 1
print(0.1 + 0.2)
print(Decimal(0.1) + Decimal(0.2))

# 변수는 메모리 공간에 값을 담아두고 불러와 사용할 수 있다.
# 변수 명명 규칙은 아래와 같다.
# 밑줄 표시는 사용해도 괜찮지만 붙임표('-', hyphen)는 사용하지 않는다.
# 숫자는 사용할 수 있지만 변수 명이 숫자로 시작하면 안 된다.
# 읽기 쉽도록 소문자를 이용하고 단어들을 밑줄 표시로 구분한다.
filename = 'budget.csv'

# 만약 문자열 안에 따옴표가 쓰여야 한다면 다음과 같이 피할 수 있다.
# 큰 따옴표와 작은 따옴표를 혼용하거나, 백슬래시를 사용한다.
"A recipe isn't just a list of ingredients."
'A recipe isn\'t just a list of ingredients.'

# 리스트
# 순서가 있으며 타입에 상관없이 넣을 수 있다.
['milk', 'lettuce', 'eggs']
[1.0, 5, 10.0, 0]

shopping_list = ['milk', 'lettuce', 'eggs']
print(shopping_list)

cats = 2
dogs = 5
horses = 1
animal_counts = [cats, dogs, horses]
print(animal_counts)

cat_names = ['Walter', 'Ra']
dog_names = ['Joker', 'Simon', 'Ellie', 'Lishka', 'Fido']
horse_names = ['Mr. Ed']
animal_names = [cat_names, dog_names, horse_names]
print(animal_names)

# 딕셔너리
# key, value로 이루어져 있다.
animal_counts = {'cats': 2, 'dogs': 5, 'horses': 1}
print(animal_counts['dogs'])

animal_names = {
    'cats': ['Walter', 'Ra'],
    'dogs': ['Joker', 'Simon', 'Ellie', 'Lishka', 'Fido'],
    'horses': ['Mr. Ed']
}

# 문자열 메서드
filename = '         budget.csv'
print(filename)
print(filename.strip())

filename = 'budget.csv'
print(filename.upper())

filename = 'budget.csv'.upper()
print(filename)

print('This is ' + 'awesome.')

# 수치형 메서드
answer = 40 + 2
print(answer)
answer = 40 ** 2
print(answer)

# 리스트 메서드
print(['Joker', 'Simon', 'Ellie'] + ['Lishka', 'Turtle'])
# 하지만 - 는 되지 않는다. 타입별로 지원하는 액션에 대해서는 알아둘 필요가 있다.
dog_names = []
dog_names.append('Joker')
print(dog_names)
dog_names.remove('Joker')
print(dog_names)

# 딕셔너리 메서드
animal_counts = {}
animal_counts['horses'] = 1
animal_counts['cats'] = 2
animal_counts['dogs'] = 5
animal_counts['snakes'] = 0
print(animal_counts)
print(animal_counts.keys())
print(animal_counts['dogs'])

dogs = animal_counts['dogs']
print(dogs)

# type 메서드
# 타입을 알려준다.
print(type('20011'))
print(type(20011))

# dir
# 데이터 유형과 관련된 모든 내장 메서드와 속성 확인 가능
print(dir('cat,dog,horse'))
# __ 로 시작하는 경우 내부 혹은 프라이빗 메서드를 나타낸다.
print('cat,dog,horse'.split(','))
print(dir(['cat', 'dog', 'horse']))

animals = ['cat', 'dog', 'horse']
print(dir(animals))
animals.reverse()
print(animals)
animals.sort()
print(animals)

# help
# 메서드 도움말을 검색할 수 있다.
animals = 'cat,dog,horse'
help(animals.split)










