"""
책에 나오는 pdftables의 경우 그 당시에도 업데이트가 되지 않는 상태였고,
3.x에서는 더더욱 동작하지 않는다.

pip install camelot-py
pip install tabula-py 를 이용한다.
https://www.thepythoncode.com/article/extract-pdf-tables-in-python-camelot
dependencies 설치
https://camelot-py.readthedocs.io/en/master/user/install-deps.html#install-deps

예제는 책이 아닌 블로그로 사용한다.

pdf의 경우 저자가 설명했듯 아직까지도 인식률이 좋지 못하다.
OpenCV를 이용하여 여러가지 시도를 하고 있지만 유료 소프트웨어도 그럴싸한 결과를 내지 못하는 실정이다.
"""
import camelot

tables = camelot.read_pdf('foo.pdf')

# 테이블 개수
print("Total tables extracted:", tables.n)

# 첫 번째 테이블을 pandas의 dataframe으로 반환
print(tables[0].df)

# 원하는 형식으로 자유롭게 저장이 가능
tables[0].to_csv('foo.csv')
tables[0].to_excel('foo.xlsx')
# 전체를 zip으로 반환 가능
tables.export('foo.csv', f='csv', compress=True)
# HTML 으로도 가능
tables.export('foo.html', f='html')
