"""
중복 기록 처리하기
중복 기록을 삭제하고 사용하지 않으려면 큰 문제는 없다.
하지만 때때로 중복 기록을 보존하고 싶다면 그 방법을 알아둬야 한다.
"""
from csv import DictReader
import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

mn_data_rdr = DictReader(open(os.path.join(data_dir, 'unicef', 'mn.csv'), 'r'))

mn_data = [d for d in mn_data_rdr]


def combine_data_dict(data_rows):
    data_dict = {}
    for row in data_rows:
        key = f'{row.get("HH1")}-{row.get("HH2")}'
        if key in data_dict.keys():
            data_dict[key].append(row)
        else:
            data_dict[key] = [row]
    return data_dict


mn_dict = combine_data_dict(mn_data)
print(len(mn_dict))
