# 헤더를 미리 재배열 한 코드
from csv import reader
import os
import pickle

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
        index = data_rows[0].index(header)
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

# 리스트에서 zip object를 꺼내고
# 리스트로 형변환을 해버리면 해당 객체의 데이터가 날아가는 것을 알 수 있다.
# print(list(zipped_data[0]))
# print(zipped_data[0])
# print(list(zipped_data[0]))
#
# print(zipped_data[1])
# print(list(zipped_data[1]))
# print(list(zipped_data[1]))


# zipped_data는 이후 코드에서 불러와 사용된다.
# 파일을 import 하게되면 매번 해당 파일의 로직을 돌려야하기 떄문에
# 저장을 하여 사용할 예정이다.
# 텍스트가 아닌 바이너리를 저장해서 사용하는 방법은 pickle 라이브러리를 사용하는 것이다.
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zipped_data.pickle'), 'wb') as f:
    pickle.dump(zipped_data, f)
