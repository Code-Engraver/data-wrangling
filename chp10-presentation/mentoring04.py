# 지도 그리기
# 책에서 설치하라고 한 라이브러리만 설치하게 되면 오류를 발생시킨다.
# brew install cairo 를 이용해서 해결이 가능하다.
import os
import json
import pickle
import agate
import pygal

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# 매칭이 안된 국가들을 찾아서 클리닝한 파일을 로드한다.
with open(os.path.join(data_dir, 'chp10', 'iso-2-cleaned.json'), 'r') as f:
    country_codes = json.load(f)

country_dict = {}
for c in country_codes:
    country_dict[c.get('name')] = c.get('alpha-2')


def get_country_code(row):
    return country_dict.get(row['Countries and areas'])


with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ranked.pickle'), 'rb') as f:
    ranked = pickle.load(f)

ranked = ranked.compute([('country_code', agate.Formula(agate.Text(), get_country_code)), ])

for r in ranked.where(lambda x: x.get('country_code') is None).rows:
    print(r['Countries and areas'])

worldmap_chart = pygal.maps.world.World()
worldmap_chart.title = 'Child Labor Worldwide'

cl_dict = {}
for r in ranked.rows:
    cl_dict[r.get('country_code').lower()] = r.get('Total (%)')

worldmap_chart.add('Total Child Labor (%)', cl_dict)
worldmap_chart.render()

worldmap_chart.render_to_file('world_map.svg')
worldmap_chart.render_to_png('world_map.png')
