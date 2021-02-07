"""
터미널에서 sqlite3 data_wrangling.db 입력 시 파일 생성
터미널에서 나오는 방법은 .q

본 예제에서는 dataset이라는 라이브러리가 table의 스키마를 알아서 잡아주고
쉽게 insert 할 수 있도록 되어있지만
실제로 DB를 사용하기 위해서는 조금 더 자세한 내용이 필요하긴 하다.

여기에서는 table 이라는 개념과 키-값의 모음이 한 행을 이룬다는 사실만 알고 넘어가자.
"""
import dataset

db = dataset.connect("sqlite:///data_wrangling.db")

my_data_source = {
    'url': 'http://www.tsmplug.com/football/premier-league-player-salaries-club-by-club/',
    'description': 'Premier League Club Salaries',
    'topic': 'football',
    'verified': False
}

table = db['data_sources']
table.insert(my_data_source)

another_data_source = {
    'url': 'http://www.premierleague.com/content/premierleague/en-gb/players/index.html',
    'description': 'Premier League Stats',
    'topic': 'football',
    'verified': True
}

table.insert(another_data_source)

source = db['data_sources'].all()

for test in source:
    print(test)
