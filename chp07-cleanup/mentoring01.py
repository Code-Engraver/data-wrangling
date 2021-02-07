"""
데이터 클리닝은 데이터 랭글링에 있어 필수적인 작업이다.
데이터를 클리닝하고 비일관성이나 가독성과 같은 문제를 해결해야 한다.
이는 두 개 이상의 데이터세트를 적절하게 결합해 유용하게 쓸 수 있게 해준다.
연구 결과 발표와 함께 데이터를 공개할 때는 클리닝된 데이터와 방법을 함께 공개하는 것이 좋다.

이번 데이터는 유니세프 보고서에 사용된 초기 데이터 세트이다.
MICS(Multiple Indicator Cluster Surveys, 다수지표군조사)의 결과물이다.
전 세계의 여성 및 아동의 생활 조건을 조사하기 위한 가계 수준의 설문조사로,
유니세프의 직원과 자원봉사자들에 의해 실시되었다.

대부분의 MICS 미가공 데이터는 SPSS 형식 또는 .sav 파일로 제공된다.
책의 저자는 SPSS 형식의 파일을 csv 로 변환시켜 두었다.
"""
from csv import DictReader, reader
import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

data_rdr = DictReader(open(os.path.join(data_dir, 'unicef', 'mn.csv'), 'r'))
header_rdr = DictReader(open(os.path.join(data_dir, 'unicef', 'mn_headers.csv'), 'r'))

data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr]

# 'HH1': '1'
# {'Name': 'HH1', 'Label': 'Cluster number', 'Question': ''}
# 헤더 부분이 약자로 되어있다.
# HH1 은 Cluster number 를 나타낸다.
# print(data_rows[:5])
# print(header_rows[:5])

# 약자와 풀 네임을 매칭 시키는 방법
for data_dict in data_rows:
    # data_dict => {'': '1', 'HH1': '1', 'HH2': '17', 'LN': '1', 'MWM1': '1', 'MWM2': '17', 'MWM4': '1' ......}
    for dkey, dval in data_dict.items():
        # dkey => HH1 / dval => 1
        # header_dict => {'Name': 'HH1', 'Label': 'Cluster number', 'Question': ''}
        for header_dict in header_rows:
            # hkey => Name / hval => HH1
            for hkey, hval in header_dict.items():
                if dkey == hval:
                    # print('match!')
                    pass

# 헤더를 교체하는 방법 1
new_rows = []
for data_dict in data_rows:
    new_row = {}
    for dkey, dval in data_dict.items():
        for header_dict in header_rows:
            if dkey in header_dict.values():
                new_row[header_dict.get('Label')] = dval
    new_rows.append(new_row)

# print(new_rows[0])
