"""
정부 부패(혹은 국민들이 인식하는 정부 부패)가 아동 노동률에 영향을 미칠까?
국제 투명성 기구의 부패 인식 지수 데이터와
유니세프의 아동 노동 데이터를 비교해본다.
"""
import os
import xlrd
import agate
import pickle

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

cpi_workbook = xlrd.open_workbook(os.path.join(data_dir, 'chp9', 'corruption_perception_index.xls'))
cpi_sheet = cpi_workbook.sheets()[0]

# 전체 행을 출력하여 타이틀의 행을 알아본다.
# 타이틀은 1, 2 인덱스에 있다.
# for r in range(cpi_sheet.nrows):
#     print(r, cpi_sheet.row_values(r))

# title 리스트를 만든다.
cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
cpi_title_rows = list(cpi_title_rows)
cpi_titles = [t[0] + " " + t[1] for t in cpi_title_rows]
cpi_titles = [t.strip() for t in cpi_titles]

# 데이터 리스트를 만든다.
cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]


# 타입 리스트를 만든다.
def get_types(example_row):
    types = []
    for v in example_row:
        value_type = xlrd.sheet.ctype_text[v.ctype]
        if value_type == 'text':
            types.append(agate.Text())
        elif value_type == 'number':
            types.append(agate.Number())
        elif value_type == 'xldate':
            types.append(agate.Date())
        else:
            types.append(agate.Text())
    return types


# 만들어진 데이터 리스트와 타입 리스트, 제목 리스트를 사용하여
# agate Table을 만들어 반환한다.
def get_table(new_arr, types, titles):
    try:
        table = agate.Table(new_arr, titles, types)
        return table
    except Exception as e:
        print(e)


# 타이틀 리스트에 불량 타이틀이 존재한다.
# Country Rank 열이 두개 존재한다.
cpi_titles[0] = cpi_titles[0] + ' Duplicate'

cpi_types = get_types(cpi_sheet.row(3))


def get_new_array(old_array, function_to_clean):
    new_arr = []
    for row in old_array:
        cleaned_row = [function_to_clean(rv) for rv in row]
        new_arr.append(cleaned_row)
    return new_arr


# 책에는 누락되어 있다.

# 파이썬 2.x의 코드
# def float_to_str(val):
#     if isinstance(val, float):
#         return str(val)
#     elif isinstance(val, (str, unicode)):
#         print 'unicode is', val.encode('utf-8')
#         return val.encode('ascii', errors='replace').strip()
#     return val

# 파이썬 3.x의 코드
def float_to_str(val):
    if isinstance(val, float):
        return str(val)
    elif isinstance(val, str):
        return val
    else:
        raise Exception

# 2.x와 3.x의 차이가 나는 이유는 데이터 타입이 다르기 떄문이다.
# 파이썬2의 문자 타입은 str: raw 8 bit, unicode: unicode 문자
# 파이썬3의 문자 타입은 bytes : raw 8 bit, str : unicode 문자

# 파이썬 3에서는 bytes와 str을 함께 사용할 수 없다.
# 파이썬 2에서는 7 bit ascii 사용 시 연산자에 str과 unicode 인스턴스를 동시에 사용이 가능하다.
# 그래서 본 책에서는 2.x와 같은 코드를 만든것이다.


cpi_rows = get_new_array(cpi_rows, float_to_str)

cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

# agate 라이브러리의 join
# SQL과 비슷
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ranked.pickle'), 'rb') as f:
    ranked = pickle.load(f)

cpi_and_cl = cpi_table.join(ranked, 'Country / Territory', 'Countries and areas', inner=True)
print(cpi_and_cl.column_names)

for r in cpi_and_cl.order_by('CPI 2013 Score').limit(10).rows:
    print(f'{r["Country / Territory"]}: {r["CPI 2013 Score"]} - {r["Total (%)"]}%')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cpi_and_cl.pickle'), 'wb') as f:
    pickle.dump(cpi_and_cl, f)
