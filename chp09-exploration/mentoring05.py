# 데이터 분석하기

# 데이터 탐색과 데이터 분석의 차이점
# 데이터 분석은 질문에 대한 답을 찾는 과정이다.
# 데이터 탐색은 데이터 세트의 추세나 속성을 알아보는 것을 의미한다.

# 왜 아프리카에 아동 노동이 더 성행할까?
# 아시아와 남아메리카 대륙에 존재하는 아동 노동 이상치는 무엇인가?
# 국민의 부패인식도와 아동 노동이 어떻게 연관되어 있나?
import os
import pickle
import numpy
import agate

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cpi_and_cl_2.pickle'), 'rb') as f:
    cpi_and_cl = pickle.load(f)

africa_cpi_cl = cpi_and_cl.where(lambda x: x['continent'] == 'africa')

for r in africa_cpi_cl.order_by('Total (%)', reverse=True).rows:
    print(f"{r['Country / Territory']}: {r['Total (%)']}% - {r['CPI 2013 Score']}")
print()

print(
    numpy.corrcoef(
        [float(t) for t in africa_cpi_cl.columns['Total (%)'].values()],
        [float(c) for c in africa_cpi_cl.columns['CPI 2013 Score'].values()]
    )[0, 1]
)
print()

africa_cpi_cl = africa_cpi_cl.compute([('Africa Child Labor Rank', agate.Rank('Total (%)', reverse=True)), ])
africa_cpi_cl = africa_cpi_cl.compute([('Africa CPI Rank', agate.Rank('CPI 2013 Score')), ])

# 전체 데이터를 대상으로 상관 관계를 판단했을 때보다 상관 계수가 감소했다.
# 이는 아프리카 데이터만을 살펴 보면 아동 노동과 국민의 부패인식도가 좀 더 밀접한 관계를 나타낸다는 것을 의미한다.

# 부패 인식도와 아동 노동 백분율의 평균값을 찾고 가장 높은 아동 노동률과 최악의 부패 인식도를 보유한 국가르 찾아보자
cl_mean = africa_cpi_cl.aggregate(agate.Mean('Total (%)'))
cpi_mean = africa_cpi_cl.aggregate(agate.Mean('CPI 2013 Score'))


def highest_rates(row):
    if row['Total (%)'] > cl_mean and row['CPI 2013 Score'] < cpi_mean:
        return True
    return False


highest_cpi_cl = africa_cpi_cl.where(lambda x: highest_rates(x))

for r in highest_cpi_cl.rows:
    print(f"{r['Country / Territory']}: {r['Total (%)']}% - {r['CPI 2013 Score']}")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'africa_cpi_cl.pickle'), 'wb') as f:
    pickle.dump(africa_cpi_cl, f)
