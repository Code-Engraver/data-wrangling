"""
데이터에 어떠한 추세가 존재하지 않는다는 것을 알게 되거나 예상치 못한 추세를 발견하게 되는 것은 재미있는 일이다.
모든 것이 우리가 예상한 대로라면 데이터 랭글링은 꽤 지루한 작업이 될 것이다.
예측은 적게 하고 탐색은 많이 해야 한다.
"""
import os
import xlrd
import agate
import pickle

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

workbook = xlrd.open_workbook(os.path.join(data_dir, 'chp9', 'unicef_oct_2014.xls'))

print(f'엑셀 내 시트 개수: {workbook.nsheets}')
print(f'시트 이름 리스트: {workbook.sheet_names()}')
print()

sheet = workbook.sheets()[0]
print(f'시트 내 행 개수: {sheet.nrows}')
print(f'시트의 첫 행 추출: {sheet.row_values(0)}')
print()

# 행을 순회하면서 출력
# for r in range(sheet.nrows):
#     print(r, sheet.row(r))

# 한 행만 선택했다면 놓쳤을 정보를 두 행을 모두 이용하여 얻을 수 있었다.
# 시간을 좀 더 할애하여 이 부분을 개선할 수 있겠지만
# 일단 데이터에 대한 초기 탐사치고는 괜찮은 결과를 얻었다.
title_rows = zip(sheet.row_values(4), sheet.row_values(5))
title_rows = list(title_rows)
print(title_rows)
print()

# 튜플의 값을 읽기 쉽도록 공백으로 연결한 뒤
# 좌우 공백을 제거한다.
# 타이틀 리스트가 완료되었다.
titles = [t[0] + ' ' + t[1] for t in title_rows]
print(titles)
titles = [t.strip() for t in titles]
print()

# 타이틀이 분류되었으니 엑셀 파일의 어떤 행을 사용할지 결정
# 시트에는 국가 그리고 대륙 데이터가 담겨 있는데, 국가 데이터를 중점적으로 살펴보자.
country_rows = [sheet.row_values(r) for r in range(6, 114)]

# xlrd 내장 기능을 사용하여 데이터를 파악한다.
text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()

example_row = sheet.row(6)

# xlrd 만을 이용해도 데이터 타입이 잘 매칭되어 있는 것을 확인할 수 있다.
print(example_row)
# 데이터 타입을 숫자로 나타낸다.
# xlrd.sheet.ctype_text 를 출력해보면 해당 숫자의 의미를 알 수 있다.
# {0: 'empty', 1: 'text', 2: 'number', 3: 'xldate', 4: 'bool', 5: 'error', 6: 'blank'}
print(example_row[0].ctype)
print(example_row[0].value)
print(xlrd.sheet.ctype_text)
print()

# row 를 순회하면서 agate 라이브러리에 사용할 유형 리스트를 만든다.
# v.ctype 의 숫자를 dict에 매칭하여 읽기 쉽도록 한다.
# 라이브러리 도움말에 명시된 바와 같이 유형이 매칭되지 않으면 텍스트 열 유형을 이어 붙인다.
types = []
for v in example_row:
    value_type = xlrd.sheet.ctype_text[v.ctype]
    if value_type == 'text':
        types.append(text_type)
    elif value_type == 'number':
        types.append(number_type)
    elif value_type == 'xldate':
        types.append(date_type)
    else:
        types.append(text_type)


# agate의 table로 만들기 전에 불량 데이터를 정제해야 한다.
# 데이터 어딘가에 널 값을 '-' 가 들어있는 데이터가 존재한다.
def remove_bad_chars(val):
    if val == '-':
        return None
    return val


cleaned_rows = []
for row in country_rows:
    cleaned_row = [remove_bad_chars(rv) for rv in row]
    cleaned_rows.append(cleaned_row)


# 함수를 만들고 해당 함수를 리스트에 적용하여 cleaned 데이터를 얻어내는 방식은
# 추후에 사용될 가능성이 있으므로 좀 더 추상적이고 제네릭한 헬퍼 함수를 만들어보자
# 좀 더 추상적이고 제네릭한 헬퍼 함수를 만들어 보자.
def get_new_array(old_array, function_to_clean):
    new_arr = []
    for row in old_array:
        cleaned_row = [function_to_clean(rv) for rv in row]
        new_arr.append(cleaned_row)
    return new_arr


cleaned_rows = get_new_array(country_rows, remove_bad_chars)

# agate를 이용하여 테이블을 생성한다.
table = agate.Table(cleaned_rows, titles, types)
print(table)
print()
table.print_table(max_columns=7)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'table.pickle'), 'wb') as f:
    pickle.dump(table, f)
