"""
이상치와 불량 데이터 찾기
이상치와 불량 데이터를 찾는 것이 데이터 클리닝에서 가장 어려운 작업니다.
통계에 대한 이해도가 필요하고, 많은 행 속에서 불량을 찾아낼 수 있는 코드도 필요하다.
또한 이상치와 불량 데이터를 찾아내고 지울 때는 그에 따른 보고서가 필요할 수 있다.
"""
import os
import pickle
import numpy as np

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zipped_data.pickle'), 'rb') as f:
    zipped_data = pickle.load(f)

# zip object를 꺼내서 해제하면 데이터가 유실되는 문제 해결
new_zipped_data = []
for x in zipped_data:
    new_zipped_data.append(list(x))

# 중복 기록 찾기
# 동일한 설문조사에 기반한 두 개 이상의 데이터 세트를 사용하고 있거나
# 사용하고 있는 비가공 데이터에 중복 행이 포함되어 있을 가능성이 높다면
# 중복 기록을 반드시 제거하여 데이터를 올바르게 사용해야 한다.
# 고유 식별자를 이용하면 더 쉽게 중복 기록을 찾을 수 있다.

# set을 이용한 고유 값 찾기
list_with_dupes = [1, 5, 6, 2, 5, 6, 8, 3, 8, 3, 3, 7, 9]

set_without_dupes = set(list_with_dupes)
print(set_without_dupes)
print()

# set을 이용하면 집합 처럼 빠른 비교가 가능해진다.
first_set = set([1, 5, 6, 2, 6, 3, 6, 7, 3, 7, 9, 10, 321, 54, 654, 432])
second_set = set([4, 6, 7, 432, 6, 7, 4, 9, 0])

print(first_set.intersection(second_set))
print(first_set.union(second_set))
print(first_set.difference(second_set))
print(second_set - first_set)
print(6 in second_set)
print(0 in first_set)
print()

# numpy 이용한 고유 값 찾기
list_with_dupes = [1, 5, 6, 2, 5, 6, 8, 3, 8, 3, 3, 7, 9]
print(np.unique(list_with_dupes, return_index=True))
array_with_dupes = np.array([[1, 5, 7, 3, 9, 11, 23], [2, 4, 6, 8, 2, 8, 4]])
print(np.unique(array_with_dupes))
print()

# 군집 번호(Cluster number), 가구 번호(Household number), 개인 줄 번호(Man's line number) 가
# 고유한 값을 가질 수 있고, 키로 사용될 수 있을 것으로 예상할 수 있다.
for x in enumerate(new_zipped_data[0]):
    print(x)

# Line number 을 검사해본다.
# KeyError가 발생하는 것을 보니 중복 기록이 존재한다.
# set_of_lines = set([x[2][1] for x in new_zipped_data])
# uniques = [x for x in new_zipped_data if not set_of_lines.remove(x[2][1])]
# print(set_of_lines)

# 지저분하거나 고유 키가 뚜렷하게 눈에 띄지 않는 데이터 세트를 처리할 경우에도
# 고유 키를 찾아 비교하는 것이 좋다.

# 군집, 가구, 줄 번호의 조합으로 고유 키를 생성할 수 있다.
# 코드의 결과를 보면 KeyError 도 발생하지 않고, 전체가 삭제된 것을 볼 수 있다.
set_of_keys = set([f'{x[0][1]}-{x[1][1]}-{x[2][1]}' for x in new_zipped_data])
uniques = [x for x in new_zipped_data if not set_of_keys.remove(f'{x[0][1]}-{x[1][1]}-{x[2][1]}')]
print(len(set_of_keys))
