# 상관관계 판별
# agate 라이브러리에는 데이터 세트에 대한 간단한 통계적 분석을 실시할 때 사용할 수 있는 도구들이 있다.
# 정부 부패에 대한 인식과 아동 노동률 간 상관관계가 존재하는지 알아보자.

# 피어슨 상관 관계
# 상관 계수는 데이터에 상관관계가 존재하는지, 특정 변수가 다른 변수에 미치는 영향이 있는지 판단하는데 사용된다.
import numpy
import os
import pickle
import agate
import agatestats
import json

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cpi_and_cl.pickle'), 'rb') as f:
    cpi_and_cl = pickle.load(f)

# -0.36024907120356714
# 약한 음의 상관관계를 확인할 수 있다.
# 두 변수가 음의 상관관계를 가진다는 것은 한 변수가 증가할 때 다른 변수는 감소한다는 것을 의미한다.
# 두 변수가 양의 상관관계를 가진다는 것은 두 변수가 함께 증가하거나 감소한다는 것을 의미한다.
# 피어슨 상관계수는 -1과 1 사이의 값을 가지는데, 0일 때는 상관관계가 없다는 것을 의미하고,
# -1이나 1일 때는 매우 밀접한 상관관계를 가진다는 것을 의미한다.
print(
    numpy.corrcoef(
        [float(t) for t in cpi_and_cl.columns['Total (%)'].values()],
        [float(s) for s in cpi_and_cl.columns['CPI 2013 Score'].values()]
    )[0, 1]
)

# 이상치 판별하기
# 특정 데이터 행과 데이터세트의 다른 행들 간에 두드러진 차이가 존재한다면 이상치가 존재한다고 할 수 있다.
# 어떤 때는 이상치는 전체 이야기의 일부만을 들려 주기 때문에 이상치를 제거하면 중요한 추세를 발견하게 될 수도 있다.
# 그러나 이상치가 그 자체만으로 의미를 가질 때도 있다.

# 이상치를 찾는 방법은 두 가지가 존재한다.
# 하나는 표준편차를 이용하는 것이고, 다른 하나는 중위수 절대 편차를 이용하는 것이다.
# 두 가지 방법을 모두 사용하여 분산 및 표준 편차를 분석해 보면 데이터세트의 여러 양상을 확인할 수 있다.

# agate의 table의 표준 편차 이상치 메서드는 평균의 적어도 3 표준 편차 범위 이내에 존재하는 값들로 구성된 표를 반환한다.

# deviations: 편차의 수, reject: True(이상치가 아닌 값만), False(이상치만)
std_dev_outliers = cpi_and_cl.stdev_outliers('Total (%)', deviations=3, reject=False)

print(len(std_dev_outliers.rows))

std_dev_outliers = cpi_and_cl.stdev_outliers('Total (%)', deviations=5, reject=False)

print(len(std_dev_outliers.rows))

# 편차의 수를 3으로 뒀을 때와 5로 뒀을 때 개수의 변화가 없다는 것은 분산을 잘 파악하지 못했다는 의미이다.
# 실제 데이터의 분산을 알아내기 위해서 관심 있는 국가들만을 포함하도록 데이터를 정제해야 할지 탐색해 보아야 한다.
# 평균 절대 편차를 이용하여 Total (%) 열의 분산을 알아보자.
mad = cpi_and_cl.mad_outliers('Total (%)')

# 발견되는 이상치가 줄었지만 이상한 결과 리스트를 얻었다.
# 리스트를 살펴보면 샘플에서 가장 높은 값이나 낮은 값이 포함되어 있지 않다.
# 이를 통해 우리가 가진 데이터세트가 이상치 판별을 위한 일반적인 통계적 규칙을 따르지 않는다는 것을 알 수 있다.
for r in mad.rows:
    print(r['Country / Territory'], r['Total (%)'])

# 데이터 세트를 그룹화하고 그룹 간의 관계를 탐색해보자
# 대륙을 기준으로 데이터를 그룹화하여 부패인식도 데이터와의 상관관계가 존재하는지 확인하고 끌어낼 수 있는 결론이 있는지 살펴보자
with open(os.path.join(data_dir, 'chp9', 'earth.json'), 'r') as f:
    country_json = json.load(f)

country_dict = {}
for dct in country_json:
    country_dict[dct['name']] = dct['parent']


def get_country(country_row):
    return country_dict.get(country_row['Country / Territory'].lower())


# 잘못된 부분이 존재
# cpi_and_cl = cpi_and_cl.compute([('continent', agate.Formula(agate.Text(), get_country))])

# 잘못된 부분이 없는지 확인
# for r in cpi_and_cl.rows:
#     print(r['Country / Territory'], r['continent'])

# 일부 국가에 None 유형이 있는 것으로 보아 손실 자료가 존재한다.
# 손실 자료만 뽑아서 확인해보면 매칭되지 않은 국가는 많지 않다.
# earth.json 파일을 클리닝 하는 것을 권장한다.
# no_continent = cpi_and_cl.where(lambda x: x['continent'] is None)
#
# for r in no_continent.rows:
#     print(r['Country / Territory'])

# 클리닝된 대륙 데이터
with open(os.path.join(data_dir, 'chp9', 'earth-cleaned.json'), 'r') as f:
    country_json = json.load(f)

country_dict = {}
for dct in country_json:
    country_dict[dct['name']] = dct['parent']

cpi_and_cl = cpi_and_cl.compute([('continent', agate.Formula(agate.Text(), get_country))])

grp_by_cont = cpi_and_cl.group_by('continent')
print(grp_by_cont)

for cont, table in grp_by_cont.items():
    print(cont, len(table.rows))

# 눈으로 확인했을 때 아프리카와 아시아가 높은 값을 가지는 것을 확인할 수 있다.
# 하지만 이것만으로 데이터에 접근하기엔 쉽지 않다.
# 이 때 필요한 것이 집계 메서드이다.
# 국민들이 인식하는 정부 부패 및 아동 노동과 관련하여 대륙들이 어떻게 다른지 비교해보자.
agg = grp_by_cont.aggregate([
    ('cl_mean', agate.Mean('Total (%)')),
    ('cl_max', agate.Max('Total (%)')),
    ('cpi_median', agate.Median('CPI 2013 Score')),
    ('cpi_min', agate.Min('CPI 2013 Score'))
])
agg.print_table()
print()
agg.print_bars('continent', 'cl_max')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cpi_and_cl_2.pickle'), 'wb') as f:
    pickle.dump(cpi_and_cl, f)
