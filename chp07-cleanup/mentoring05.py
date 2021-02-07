"""
데이터를 서식화 하는 부분에 대한 코드이다.

불필요한 공백을 없애고, 날짜를 변환하는 등의 작업을 할 수 있다.
"""
import os
import pickle
from datetime import datetime

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zipped_data.pickle'), 'rb') as f:
    zipped_data = pickle.load(f)

# zip object를 꺼내서 해제하면 데이터가 유실되는 문제 해결
zipped_data_first = []
for x in zipped_data[0]:
    zipped_data_first.append(x)

for x in zipped_data_first:
    print(f'Question: {x[0]}\nAnswer: {x[1]}')

for x in zipped_data_first:
    print(f'Question: {x[0][1]}\nAnswer: {x[1]}')
print()

# 데이터에 다양한 서식을 부여하여 출력할 수 있다.
example_dict = {
    'float_number': 1324.321325493,
    'very_large_integer': 43890923148390284,
    'percentage': .324,
}

string_to_print = 'float: {float_number:.4f}\n'
string_to_print += 'integer: {very_large_integer:,}\n'
string_to_print += 'percentage: {percentage:.2%}'

print(string_to_print.format(**example_dict))
print()

for x in enumerate(zipped_data_first[:20]):
    print(x)
print()

# 문자열로 되어있는 날짜를 datetime 객체로 변환하여 각종 계산을 할 수 있다.
start_string = f'{zipped_data_first[8][1]}/{zipped_data_first[7][1]}/{zipped_data_first[9][1]} ' \
               f'{zipped_data_first[13][1]}:{zipped_data_first[14][1]}'
print(start_string)
start_time = datetime.strptime(start_string, '%m/%d/%Y %H:%M')
print(start_time)
print()

end_time = datetime(int(zipped_data_first[9][1]), int(zipped_data_first[8][1]), int(zipped_data_first[7][1]),
                    int(zipped_data_first[15][1]), int(zipped_data_first[16][1]))

print(end_time)
print()

duration = end_time - start_time
print(duration)
print(duration.days)
print(duration.total_seconds())
minutes = duration.total_seconds() / 60
print(minutes)
print()

print(end_time.strftime('%m/%d/%Y %H:%M:%S'))
print(start_time.ctime())
print(start_time.strftime('%Y-%m-%dT%H:%M:%S'))
