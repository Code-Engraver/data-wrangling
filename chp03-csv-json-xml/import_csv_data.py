"""
CSV 파일은 데이터 열을 쉼표로 구분하는 파일이다.
TSV 파일 또한 CSV 파일의 부류로 여겨지는데 차이점은 데이터 열을 탭으로 구분한다.
데이터 열을 구분 짓는 방법은 파일 확장자에 있을 수 있지만 없을 수도 있다.
"""
import csv
import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# reader 자체를 반복문에 돌리기 위해서는 file io 가 close 되면 안된다.
with open(os.path.join(data_dir, 'chp3', 'data-text.csv'), 'r') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        print(row)
