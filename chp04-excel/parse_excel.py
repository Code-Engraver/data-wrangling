"""
xlrd 를 이용하여 xlsx 파일을 읽는 것은 1.2.0 버젼까지 가능하다.
현재는 2.0.1 버전이기에 에러가 송출될 것이다.
pip install xlrd==1.2.0 을 이용하여 알맞은 버젼을 설치하면 실행된다.
"""
import xlrd
import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

book = xlrd.open_workbook(os.path.join(data_dir, 'chp4', 'SOWC 2014 Stat Tables_Table 9.xlsx'))

# 시트명을 출력가능
# for sheet in book.sheets():
#     print(sheet.name)

sheet = book.sheet_by_name("Table 9 ")

# 전체 행 수 출력 가능
# print(sheet.nrows)

data = {}
for i in range(14, sheet.nrows):
    # 14번째까지는 쓸모없다.
    row = sheet.row_values(i)

    country = row[1]

    data[country] = {
        'child_labor': {
            'total': [row[4], row[5]],
            'male': [row[6], row[7]],
            'female': [row[8], row[9]],
        },
        'child_marriage': {
            'married_by_15': [row[10], row[11]],
            'married_by_18': [row[12], row[13]],
        }
    }

    if country == "Zimbabwe":
        break

print(data)
