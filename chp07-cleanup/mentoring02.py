from csv import reader
import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# 헤더를 교체하는 방법 2
# 책에서는 data_rows의 칼럼 순서와 헤더 데이터의 순서를 맞춰서 정제를 하고자 한다.
# 그러나 159개와 210개의 갯수는 이런 식으로 맞추기에는 리스크가 있다.
# 데이터를 클리닝할 때는 확실하지 않을 땐 가장 엄격한 기준으로 하는 것이 좋다.
data_rdr = reader(open(os.path.join(data_dir, 'unicef', 'mn.csv'), 'r'))
header_rdr = reader(open(os.path.join(data_dir, 'unicef', 'mn_headers.csv'), 'r'))

data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr]

# 159개 / 210개 로 길이가 다르다.
print(len(data_rows[0]))
print(len(header_rows))

bad_rows = []

for h in header_rows:
    if h[0] not in data_rows[0]:
        bad_rows.append(h)

for h in bad_rows:
    header_rows.remove(h)

print(len(header_rows))

# 대문자 / 소문자 문제로 매칭되지 않은 경우가 있고, 필요 없는 경우가 있다.
# 또한 헤더 크롤링 당시에 발경되지 않은 항목도 있다.
# 클리닝을 한다는 것은 때때로 필요하지 않거나 클리닝이 어려운 데이터를 제거하는 것일 수도 있다.
all_short_headers = [h[0] for h in header_rows]

for header in data_rows[0]:
    if header not in all_short_headers:
        print(f'mismatch! {header}')

# 이 방법을 사용하기 위해 저자는 mn_headers_updated.csv 라는 파일을 추가한다.
