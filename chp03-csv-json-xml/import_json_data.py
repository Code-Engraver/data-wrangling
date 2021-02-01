"""
데이터 전송을 위해 가장 흔히 쓰이는 데이터 형식 가운데 하나이다.
깔끔하고 읽기 쉬우며 파싱이 용이하기 때문에 자주 쓰이게 되었다.
"""
import json
import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

with open(os.path.join(data_dir, 'chp3', 'data-text.json'), 'r') as json_file:
    data = json.loads(json_file.read())

for item in data:
    print(item)
