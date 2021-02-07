"""
이상치와 불량 데이터 찾기
이상치와 불량 데이터를 찾는 것이 데이터 클리닝에서 가장 어려운 작업니다.
통계에 대한 이해도가 필요하고, 많은 행 속에서 불량을 찾아낼 수 있는 코드도 필요하다.
또한 이상치와 불량 데이터를 찾아내고 지울 때는 그에 따른 보고서가 필요할 수 있다.
"""
import os
import pickle

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zipped_data.pickle'), 'rb') as f:
    zipped_data = pickle.load(f)

# zip object를 꺼내서 해제하면 데이터가 유실되는 문제 해결
new_zipped_data = []
for x in zipped_data:
    new_zipped_data.append(list(x))

# 첫번째 행에는 결측 데이터가 없음
for answer in new_zipped_data[0]:
    if not answer[1]:
        print(answer)

# 전체 데이터에서도 뚜렷한 결측 데이터는 존재하지 않는다.
# 그러나 이전 출력에서 NA(Not Applicable)이 존재하는 것을 알 수 있다.
# 중요한 것은 NA는 결측 데이터라고 할 수 없다.
# 하지만 NA가 차지하는 비율을 파악하고 해당 질문의 결론에 얼마나 영향을 미치는지는 파악해야 한다.
for row in new_zipped_data:
    for answer in row:
        if answer[1] is None:
            print(answer)

# 출력 결과를 통해 상당히 많은 NA가 존재하는 것을 알 수 있다.
# 이렇게 많은 비율을 차지하는 경우에는 질문이 의미가 없을 수 있다.
na_count = {}
for row in new_zipped_data:
    for resp in row:
        question = resp[0][1]
        answer = resp[1]
        if answer in ['NA', 'na', 'n/a']:
            if question in na_count.keys():
                na_count[question] += 1
            else:
                na_count[question] = 1

print(na_count)

# 유형 이상치 (type outlier)
# 숫자가 들어갈 부분에 missing 이나 NA 와 같은 문자열이 들어 있다면
# 해당 부분은 이상치 혹은 불량 데이터일 확률이 있다.
# 코드의 결과물을 보면 하나의 타입으로 추정되는 것도 있지만
# 여러 타입으로 추정되고 있는 키도 존재한다. 이런 경우에는 유형 이상치가 있을 가능성이 높다.
datatypes = {}
start_dict = {
    'digit': 0,
    'boolean': 0,
    'empty': 0,
    'time_related': 0,
    'text': 0,
    'unknown': 0
}

for row in new_zipped_data:
    for resp in row:
        question = resp[0][1]
        answer = resp[1]
        key = 'unknown'
        if answer.isdigit():
            key = 'digit'
        elif answer in ['Yes', 'No', 'True', 'False']:
            key = 'boolean'
        elif answer.isspace():
            key = 'empty'
        elif answer.find('/') > 0 or answer.find(':') > 0:
            key = 'time_related'
        elif answer.isalpha():
            key = 'text'

        if question not in datatypes.keys():
            datatypes[question] = start_dict.copy()
            datatypes[question][key] += 1

print(datatypes)

