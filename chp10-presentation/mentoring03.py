# 인터랙티브한 산점도 그리기
import os
import pickle
from bokeh.plotting import ColumnDataSource, figure, show, output_file
from bokeh.models import HoverTool

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'africa_cpi_cl.pickle'), 'rb') as f:
    africa_cpi_cl = pickle.load(f)

TOOLS = "pan,reset,hover"


def scatter_point(chart, x, y, source, marker_type):
    chart.scatter(x, y, source=source, marker=marker_type,
                  line_color="#6666ee", fill_color="#ee6666", fill_alpha=0.7, size=10)


chart = figure(title="Perceived Corruption and Child Labor in Africa", tools=TOOLS)
output_file("scatter-int_plot.html")

for row in africa_cpi_cl.rows:
    column_source = ColumnDataSource(data={'country': [row['Country / Territory']]})
    scatter_point(chart, float(row['CPI 2013 Score']), float(row['Total (%)']), column_source, 'circle')

hover = chart.select(dict(type=HoverTool))

hover.tooltips = [
    ("Country", "@country"),
    ("CPI Score", "$x"),
    ("Child Labor (%)", "$y"),
]

show(chart)
