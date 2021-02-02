"""
slate 라이브러리는 2.x 에서 릴리즈를 멈췄다. 설치하려고 하면 에러가 송출된다.
slate3k를 다운로드 받아 이를 해결할 순 있다.

slate3k는 PDF를 한 패이지식 리스트에 저장한다.
해당 타입은 str 이다.

pdf2txt.py -o en-final-table9.txt EN-FINAL\ Table\ 9.pdf
pdfminer 만 설치된 상태에서 실행하면 에러가 송출된다.
이때는 pdfminer.six 를 설치해주면 된다.
"""
import slate3k as slate
import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

with open(os.path.join(data_dir, 'chp5', 'EN-FINAL Table 9.pdf'), 'rb') as f:
    doc = slate.PDF(f)

for page in doc[:2]:
    # print(page)
    print(type(page))
