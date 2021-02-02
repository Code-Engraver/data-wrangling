"""
pdf2txt.py -o en-final-table9.txt EN-FINAL\ Table\ 9.pdf
pdfminer 만 설치된 상태에서 실행하면 에러가 송출된다.
이때는 pdfminer.six 를 설치해주면 된다.

결과가 책과는 다르게 나온 것을 알 수 있다.
개행이 더 늘어나고 인식률이 썩 좋지 못하다.
책에서 제공하는 txt 를 기준으로 진행한다.

국가
"""
import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

openfile = open(os.path.join(data_dir, 'chp5', 'en-final-table9.txt'), 'r')
country_line = total_line = False
previous_line = ''
countries = []
totals = []

double_lined_countries = [
    'Bolivia (Plurinational \n',
    'Democratic People\xe2\x80\x99s \n',
    'Democratic Republic \n',
    'Lao People\xe2\x80\x99s Democratic \n',
    'Micronesia (Federated \n',
    'Saint Vincent and \n',
    'The former Yugoslav \n',
    'United Republic \n',
    'Venezuela (Bolivarian \n',
]


def turn_on_off(target_line, status, start, prev_line, end='\n'):
    """
    This function checks to see if a line starts/ends with a certain
    value. If the line starts/ends with that value, the status is
    set to on/off (True/False).
    """
    if target_line.startswith(start):
        status = True
    elif status:
        if target_line == end and prev_line != 'and areas':
            status = False
    return status


def clean(target_line):
    """
    Cleans line breaks, spaces, and special characters from our line.
    """
    target_line = target_line.strip('\n').strip()
    target_line = target_line.replace('\xe2\x80\x93', '-')
    target_line = target_line.replace('\xe2\x80\x99', '\'')
    return target_line


for line in openfile:
    if country_line:
        if previous_line in double_lined_countries:
            line = ' '.join([clean(previous_line), clean(line)])
        countries.append(clean(line))

    elif total_line:
        if len(line.replace('\n', '').strip()) > 0:
            totals.append(clean(line))

    country_line = turn_on_off(line, country_line, 'and areas', previous_line)
    total_line = turn_on_off(line, total_line, 'total', previous_line)

    previous_line = line

data = dict(zip(countries, totals))
print(data)
