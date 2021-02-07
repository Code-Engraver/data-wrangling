"""
정기적으로 데이터세트를 업데이트하거나 데이터를 추가할 예정이라면
클리닝 과정을 최대한 효율적이고 명료하게 만들어 데이터 분석이나 결과 보고에 좀 더 많은 시간을 투자하는 편이 좋다.

데이터 정규화 및 표준화
데이터세트의 표준화 및 정규화란 가지고 있는 데이터와 진행 중인 연구의 유형에 따라
기존의 값들을 이용해 새로운 값들을 계산하는 작업을 의미할 수도 있고,
특정 열이나 값에 표준화 및 정규화 과정을 적용하는 작업을 의미할 수도 있다.
통계학적 관점에서 보면 정규화는 일반적으로 기존 데이터세트를 기반으로 새로운 값들을 계산해 내어
데이터를 특정 단위로 표준화하는 작업이다.

결과물은 DB에 넣는 코드
"""
import os
import pickle
import dataset

zipped_data_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'chp07-cleanup', 'zipped_data.pickle')

with open(zipped_data_path, 'rb') as f:
    zipped_data = pickle.load(f)

# zip object를 꺼내서 해제하면 데이터가 유실되는 문제 해결
new_zipped_data = []
for x in zipped_data:
    new_zipped_data.append(list(x))

db = dataset.connect('sqlite:///data_wrangling.db')

table = db['unicef_survey']

for row_num, data in enumerate(new_zipped_data):
    for question, answer in data:
        data_dict = {
            'question': question[1],
            'question_code': question[0],
            'answer': answer,
            'response_number': row_num,
            'survey': 'mn'
        }

        table.insert(data_dict)
