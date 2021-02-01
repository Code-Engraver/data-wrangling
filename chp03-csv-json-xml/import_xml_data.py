"""
XML은 마크업 언어이기 때문에 서식화된 데이터가 포함된 문서 구조를 가지고 있다는 것을 의미한다.
XML 문서는 기본적으로 특별한 서식을 가지고 있는 데이터 파일이다.
XML을 디자인 하는 것은 천차만별이기 때문에 잘 파악해야한다.
"""
from xml.etree import ElementTree
import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# XML을 파이썬이 이해하고 파싱할 수 있는 방식으로 저장
tree = ElementTree.parse(os.path.join(data_dir, 'chp3', 'data-text.xml'))
# XML 가장 바깥쪽의 태그 인식
root = tree.getroot()
# <Element 'GHO' at 0x104678040> 가장 바깥쪽 태그가 GHO 라는 것
# print(root)
# 하위 요소를 볼 수 있다.
# print(list(root))

data = root.find('Data')
# print(list(data))

all_data = []

for observation in data:
    record = {}
    for item in observation:
        lookup_key = list(item.attrib.keys())[0]

        if lookup_key == 'Numeric':
            rec_key = 'NUMERIC'
            rec_value = item.attrib['Numeric']
        else:
            rec_key = item.attrib[lookup_key]
            rec_value = item.attrib['Code']

        record[rec_key] = rec_value
    all_data.append(record)

print(all_data)
