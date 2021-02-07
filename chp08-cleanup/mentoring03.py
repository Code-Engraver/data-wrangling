"""
* 유니세프 데이터 파일에서 데이터를 불러온다.
* 데이터 행의 헤더를 찾는다.
* 우리가 읽을 수 있는 헤더를 수수께끼 같은 내장 헤더와 적절하게 매칭한다.
* 중복 기록이 존재하는지 확인하기 위해 데이터를 파싱한다.
* 손실 자료가 존재하는지 확인하기 위해 데이터를 파싱한다.
* 가구를 기준으로 데이터를 다른 행들과 병합한다.
* 데이터를 저장한다.

코드를 스크립트로 정리
"""
from csv import reader
import os
import dataset

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

data_rdr = reader(open(os.path.join(data_dir, 'unicef', 'mn.csv'), 'r'))
header_rdr = reader(open(os.path.join(data_dir, 'unicef', 'mn_headers_updated.csv'), 'r'))

data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr if h[0] in data_rows[0]]

all_short_headers = [h[0] for h in header_rows]

skip_index = []
final_header_rows = []

for header in data_rows[0]:
    if header not in all_short_headers:
        print(header)
        index = data_rows[0].index(header)
        if index not in skip_index:
            skip_index.append(index)
    else:
        for head in header_rows:
            if head[0] == header:
                final_header_rows.append(head)
                break

new_data = []

for row in data_rows[1:]:
    new_row = []
    for i, d in enumerate(row):
        if i not in skip_index:
            new_row.append(d)
    new_data.append(new_row)

zipped_data = []

for drow in new_data:
    zipped_data.append(zip(final_header_rows, drow))

# zip 데이터 유실 해결
new_zipped_data = []
for x in zipped_data:
    new_zipped_data.append(list(x))
zipped_data = new_zipped_data

# 결측 데이터 찾기
for x in zipped_data[0]:
    if not x[1]:
        print(x)

# 중복 데이터 찾기
set_of_keys = set([
    f'{x[0][1]}-{x[1][1]}-{x[2][1]}' for x in zipped_data
])

uniques = [x for x in zipped_data if not set_of_keys.remove(f'{x[0][1]}-{x[1][1]}-{x[2][1]}')]

print(len(set_of_keys))

# DB에 저장하기
db = dataset.connect('sqlite:///data_wrangling.db')

table = db['unicef_survey']

for row_num, data in enumerate(zipped_data):
    for question, answer in data:
        data_dict = {
            'question': question[1],
            'question_code': question[0],
            'answer': answer,
            'response_number': row_num,
            'survey': 'mn'
        }
        table.insert(data_dict)
