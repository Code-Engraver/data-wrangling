# 데이터 시각화 하기
import os
import pickle
import matplotlib.pyplot as plt
import agate

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'africa_cpi_cl.pickle'), 'rb') as f:
    africa_cpi_cl = pickle.load(f)

plt.plot(africa_cpi_cl.columns['CPI 2013 Score'], africa_cpi_cl.columns['Total (%)'])

plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title('CPI & Child Labor Correlation')

plt.show()

# 최악의 가해 국가들만 분리하여 데이터 시각화
cl_mean = africa_cpi_cl.aggregate(agate.Mean('Total (%)'))
cpi_mean = africa_cpi_cl.aggregate(agate.Mean('CPI 2013 Score'))


def highest_rates(row):
    if row['Total (%)'] > cl_mean and row['CPI 2013 Score'] < cpi_mean:
        return True
    return False


highest_cpi_cl = africa_cpi_cl.where(lambda x: highest_rates(x))

plt.plot(highest_cpi_cl.columns['CPI 2013 Score'], highest_cpi_cl.columns['Total (%)'])

plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title('CPI & Child Labor Correlation')

plt.show()
