from csv import reader
import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

data_rdr = reader(open(os.path.join(data_dir, 'unicef', 'mn.csv'), 'r'))
header_rdr = reader(open(os.path.join(data_dir, 'unicef', 'mn_headers_updated.csv'), 'r'))

data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr if h[0] in data_rows[0]]

print(len(header_rows))

all_short_headers = [h[0] for h in header_rows]
skip_index = []

for header in data_rows[0]:
    if header not in all_short_headers:
        index = data_rows[0].index(header)
        skip_index.append(index)

new_data = []

for row in data_rows[1:]:
    new_row = []
    for i, d in enumerate(row):
        if i not in skip_index:
            new_row.append(d)
    new_data.append(new_row)

zipped_data = []

for drow in new_data:
    zipped_data.append(zip(header_rows, drow))

# list로 형변환을 해줘야 출력된다.
print(list(zipped_data[0]))

data_headers = []

for i, header in enumerate(data_rows[0]):
    if i not in skip_index:
        data_headers.append(header)

header_match = zip(data_headers, all_short_headers)

# ('MHA26', 'MHA26'), ('MHA27', 'MHA27'), ('MMC1', 'MTA1'), ('MMC2', 'MTA2')
# 저자는 순서대로 묶었을 때 데이터가 잘못된 것을 찾아낸다.
# 순서만을 이용하여 매칭하기에는 쉽지 않는 부분이 존재한다는 것을 알 수 있다.
print(list(header_match))
