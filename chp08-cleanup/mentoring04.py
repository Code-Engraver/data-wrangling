"""
코드를 스크립트로 정리
함수화 진행
"""
import os
from csv import reader
import dataset


def get_rows(file_name):
    rdr = reader(open(file_name, 'r'))
    return [row for row in rdr]


def eliminate_mismatches(header_rows, data_rows):
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
    zipped_data = []
    for drow in data:
        zipped_data.append(zip(headers, drow))

    new_zipped_data = []
    for x in zipped_data:
        new_zipped_data.append(list(x))

    return new_zipped_data


def create_zipped_data(final_header_rows, data_rows, skip_index):
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
    missing_count = 0

    for response in zipped_data:
        for question, answer in response:
            if not answer:
                missing_count += 1
    return missing_count


def find_duplicate_data(zipped_data):
    set_of_keys = set([
        f'{row[0][1]}-{row[1][1]}-{row[2][1]}' for row in zipped_data
    ])
    uniques = [row for row in zipped_data if not set_of_keys.remove(f'{row[0][1]}-{row[1][1]}-{row[2][1]}')]
    return uniques, len(set_of_keys)


def save_to_sqlitedb(db_file, zipped_data, survey_type):
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
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

    data_rows = get_rows(os.path.join(data_dir, 'unicef', 'mn.csv'))
    header_rows = get_rows(os.path.join(data_dir, 'unicef', 'mn_headers_updated.csv'))

    skip_index, final_header_rows = eliminate_mismatches(header_rows, data_rows)

    zipped_data = create_zipped_data(final_header_rows, data_rows, skip_index)
    num_missing = find_missing_data(zipped_data)

    uniques, num_dupes = find_duplicate_data(zipped_data)
    if num_missing == 0 and num_dupes == 0:
        save_to_sqlitedb('sqlite:///data_wrangling.db', zipped_data, 'mn')
    else:
        error_msg = ''
        if num_missing:
            error_msg += f'We are missing {num_missing} values.'
        if num_dupes:
            error_msg += f'We have {num_dupes} duplicates.'

        error_msg += 'Please have a look and fix!'
        print(error_msg)


if __name__ == '__main__':
    main()
