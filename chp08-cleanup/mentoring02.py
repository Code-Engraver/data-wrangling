"""
데이터를 CSV 로 저장
"""
import os
import pickle
from csv import writer

zipped_data_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'chp07-cleanup', 'zipped_data.pickle')

with open(zipped_data_path, 'rb') as f:
    zipped_data = pickle.load(f)

# zip object를 꺼내서 해제하면 데이터가 유실되는 문제 해결
new_zipped_data = []
for x in zipped_data:
    new_zipped_data.append(list(x))


def write_file(target_zipped_data, file_name):
    with open(file_name, 'w') as new_csv_file:
        wrtr = writer(new_csv_file)
        titles = [row[0][1] for row in target_zipped_data[0]]
        wrtr.writerow(titles)
        for row in target_zipped_data:
            answers = [resp[1] for resp in row]
            wrtr.writerow(answers)


write_file(new_zipped_data, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cleaned_unicef_data.csv'))
