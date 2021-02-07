"""
사용법: python our_cleanup_script.py

본 스크립트는 유니세프의 남성 설문조사 데이터를 불러와서
중복 데이터 및 결측치를 확인한 뒤 헤더가 데이터와 제대로 매칭한 다음
간단한 데이터베이스 파일로 저장하기 위한것이다.
데이터와 함께 'mn.csv' 파일이 존재해야 하며
이 코드가 있는 디렉터리 내의 unicef 라는 하위 폴더 안에
'mn_updated_headers.csv' 파일이 있어야 한다.
또한 이 디렉터리의 루트에 'data_wrangling.db' fksms
SQLite 파일이 있어야 한다. 마지막으로 데이터세트 라이브러리
(http://dataset.readthedocs.org/en/latest/)를 사용한다.

만약 스크립트가 오류 없이 실행된다면, 클리닝된 데이터를
SQLite의 'unicef_survey' 테이블에 저장한다.
저장된 데이터는 다음과 같은 구조를 가진다:
    - question: 문자열
    - question_code: 문자열
    - answer: 문자열
    - response_number: 정수
    - survey: 문자열

response_number는 추후 모든 응답을 병합하는 데 사용할 수 있다.
(response_number가 3인 모든 데이터는 동일한 인터뷰에서 나온 자료 등).

문의 사항이 있는 경우 다음 연락처로 문의주시기 바랍니다...
"""
import os
from csv import reader
import dataset


def get_rows(file_name):
    """
    주어진 csv 파일명의 행으로 이루어진 리스트를 반환
    """
    rdr = reader(open(file_name, 'r'))
    return [row for row in rdr]


def eliminate_mismatches(header_rows, data_rows):
    """
    유니세프 데이터세트으로부터 헤더 행과 데이터 행이 주어졌을 때,
    건너뛸 인덱스 숫자들 리스트와 최종 헤더 행들 리스트를 반환한다.
    이 함수는 data_rows 객체의 첫 번째 원소로 헤더가 있다고 가정한다.
    또한 그 헤더들이 축약된 유니세프 형식을 따른다고 가정한다.
    그리고 헤더 데이터 안의 각 헤더 행의 첫 번째 원소가 축약된
    유니세프 형식이라고 가정한다. 그러면 데이터 행들 중 건너뛸 행(헤더와 제대로 매칭이 안되는 것들)의
    인덱스가 담긴 리스트를 첫 번째 원소로 반환하고, 최종적으로 클리닝된 헤더 행들을 두 번째 원소로 반환한다.
    """
    all_short_headers = [h[0] for h in header_rows]
    skip_index = []
    final_header_rows = []

    for header in data_rows[0]:
        if header not in all_short_headers:
            index = data_rows[0].index(header)
            if index not in skip_index:
                skip_index.append(index)
        else:
            for head in header_rows:
                if head[0] == header:
                    final_header_rows.append(head)
                    break

    return skip_index, final_header_rows


def zip_data(headers, data):
    """
    헤더 리스트와 데이터 리스트가 주어졌을 때 합친 데이터를 리스트로 반환한다.
    행별 데이터 원소들의 길이와 헤더의 길이가 동일하다고 가정한다.

    출력 예시: [(['question code', 'question summary', 'question text'], 'resp'), ....]
    """
    zipped_data = []
    for drow in data:
        zipped_data.append(zip(headers, drow))

    new_zipped_data = []
    for x in zipped_data:
        new_zipped_data.append(list(x))

    return new_zipped_data


def create_zipped_data(final_header_rows, data_rows, skip_index):
    """
    최종 헤더 행 리스트, 데이터 행 리스트, 제대로 매칭되지 않아 건너뛸
    데이터 행들의 인덱스 리스트가 주어졌을 때 데이터 행들을
    합친(매칭된 헤더와 데이터) 리스트를 반환한다. 이 함수는 데이터
    행들의 첫 번째 행이 본래의 데이터 헤더 값을 가지고 있다고 가정하며,
    그 값들을 최종 리스트에서 제거할 것이다.
    """
    new_data = []
    for row in data_rows[1:]:
        new_row = []
        for index, data in enumerate(row):
            if index not in skip_index:
                new_row.append(data)
        new_data.append(new_row)

    zipped_data = zip_data(final_header_rows, new_data)
    return zipped_data


def find_missing_data(zipped_data):
    """
    합친 데이터 집합 중에서 몇 개의 답변(answer) 값이 없는지
    개수를 세어 반환한다. 이 함수는 모든 응답이 두 번째 원소에
    저장되어 있다고 가정한다. 또한 모든 응답이 매칭된 질문, 답변
    형태로 묶여 있다고 가정한다. 정수를 반환한다.
    """
    missing_count = 0

    for response in zipped_data:
        for question, answer in response:
            if not answer:
                missing_count += 1
    return missing_count


def find_duplicate_data(zipped_data):
    """
    유니세프 zipped_data 리스트를 넣으면 고유한 원소와 중복된
    원소들의 개수를 반환한다. 이 함수는 데이터의 맨 앞 세 행이
    집, 군집, 그리고 인터뷰의 줄 번호로 구조화되어 있을 것이라고
    가정하며 이 값들을 사용해 반복이 되지 않는 고유한 키를 생성한다.
    """
    set_of_keys = set([
        f'{row[0][1]}-{row[1][1]}-{row[2][1]}' for row in zipped_data
    ])
    # 할 일: 중복 데이터가 있으면 오류가 난다.
    # 해결 방법을 찾아야 함
    uniques = [row for row in zipped_data if not set_of_keys.remove(f'{row[0][1]}-{row[1][1]}-{row[2][1]}')]
    return uniques, len(set_of_keys)


def save_to_sqlitedb(db_file, zipped_data, survey_type):
    """
    SQLite 파일 경로, 클리닝된 zipped_data, 사용된 유니세프 설문 유형을 받아
    데이터를 'unicef_survey'라는 이름의 SQLite 테이블로 저장하며
    다음과 같은 속성을 갖도록 한다.
    question, question_code, answer, response_number, survey
    """
    db = dataset.connect(db_file)

    table = db['unicef_survey']
    all_rows = []

    for row_num, data in enumerate(zipped_data):
        for question, answer in data:
            data_dict = {
                'question': question[1],
                'question_code': question[0],
                'answer': answer,
                'response_number': row_num,
                'survey': survey_type,
            }
            all_rows.append(data_dict)

    table.insert_many(all_rows)


def main():
    """
    모든 데이터를 행으로 불러오고 클리닝한 뒤, 오류가
    없으면 SQLite로 저장한다.
    오류가 발생하면 개발자들이 스트립트를 수정하거나
    데이터에 오류가 있는지 확인할 수 있도록 상세 내용을 출력한다.
    """
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

    # 할 일: 변수로 전달해 메인 함수에 다른 설문들과 함께 사용 가능하도록
    # 다음 파일들을 추상화할 필요가 있음
    data_rows = get_rows(os.path.join(data_dir, 'unicef', 'mn.csv'))
    header_rows = get_rows(os.path.join(data_dir, 'unicef', 'mn_headers_updated.csv'))

    skip_index, final_header_rows = eliminate_mismatches(header_rows, data_rows)

    zipped_data = create_zipped_data(final_header_rows, data_rows, skip_index)
    num_missing = find_missing_data(zipped_data)

    uniques, num_dupes = find_duplicate_data(zipped_data)
    if num_missing == 0 and num_dupes == 0:
        # 할 일: 이 파일도 추상화 하거나
        # 다음 코드로 넘어가기 전에 파일이 있는지 확인할 것
        save_to_sqlitedb('sqlite:///data_wrangling.db', zipped_data, 'mn')
    else:
        # 할 일: 최종적으로는 로그를 남기거나
        # 오류를 출력하기보다 이메일을 보내는 것이 나을지도
        error_msg = ''
        if num_missing:
            error_msg += f'We are missing {num_missing} values.'
        if num_dupes:
            error_msg += f'We have {num_dupes} duplicates.'

        error_msg += 'Please have a look and fix!'
        print(error_msg)


if __name__ == '__main__':
    main()
