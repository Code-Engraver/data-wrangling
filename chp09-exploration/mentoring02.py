import os
import pickle
import agate

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'table.pickle'), 'rb') as f:
    table = pickle.load(f)

# 열 목록 확인
print(table.column_names)

# 가장 높은 아동 노동률을 보유한 10개 국가를 반환한다.
most_egregious = table.order_by('Total (%)', reverse=True).limit(10)

for r in most_egregious.rows:
    print(r)
print()

# 가장 높은 소녀 노동률을 보유한 국가를 출력한다.
most_females = table.order_by('Female', reverse=True).limit(10)
for r in most_females.rows:
    print(f'{r["Countries and areas"]}: {r["Female"]}%')
print()

# 출력한 결과를 보면 백분율 값 중 None이 존재한다.
# agate 표의 where 메서드를 활용하면 이러한 값들을 제거할 수 있다.
female_data = table.where(lambda x: x['Female'] is not None)
most_females = female_data.order_by('Female', reverse=True).limit(10)

for r in most_females.rows:
    print(f'{r["Countries and areas"]}: {r["Female"]}%')
print()

# 도시의 평균 아동 노동률을 구해보자.
# 이를 위해서는 Place of residence (%) Urban 열의 평균 값을 구해야 한다.
# Null 값을 제외하고 aggregate에 Mean 함수를 넣어 계산해본다.
# 이를 이용하여 Min과 Max도 계산이 가능하다.
has_por = table.where(lambda x: x['Place of residence (%) Urban'] is not None)
print(has_por.aggregate(agate.Mean('Place of residence (%) Urban')))
print()

# 지방 아동 노동률이 50% 이상인 행 가운데 하나를 찾아 보자.
# 조건을 만족하는 첫 번째 행을 반환한다.
first_match = has_por.find(lambda x: x['Rural'] > 50)
print(first_match['Countries and areas'])
print()

# 아동 노동률이 높은 국가의 순위를 알아보자
# 이를 위해서는 Total(%) 열을 기반으로 데이터를 정렬하면 된다.
ranked = table.compute([('Total Child Labor Rank', agate.Rank('Total (%)', reverse=True)), ])
for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print(row['Total (%)'], row['Total Child Labor Rank'])
print()


# reverse를 사용하지 않고 오름차순 정렬을 하고 싶다면 역 백분율을 기준으로 열을 생성하면 된다.
def reverse_percent(row):
    return 100 - row['Total (%)']


ranked = table.compute([('Children not working (%)', agate.Formula(agate.Number(), reverse_percent))])
ranked = ranked.compute([('Total Child Labor Rank', agate.Rank('Children not working (%)')), ])

for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print(row['Total (%)'], row['Total Child Labor Rank'])

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ranked.pickle'), 'wb') as f:
    pickle.dump(ranked, f)
