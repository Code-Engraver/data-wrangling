"""
리스트로 출력하던 데이터를 딕셔너리로 변경하여 출력
"""
import csv
import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

with open(os.path.join(data_dir, 'chp3', 'data-text.csv'), 'r') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        print(row)
