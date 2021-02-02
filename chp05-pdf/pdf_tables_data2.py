import tabula
import os

tables = tabula.read_pdf("1710.05006.pdf", pages="all")

# 폴더를 만들어 저장
folder_name = "171005006-tables"
if not os.path.isdir(folder_name):
    os.mkdir(folder_name)

# 각각의 테이블을 엑셀 파일로 저장
for i, table in enumerate(tables, start=1):
    table.to_excel(os.path.join(folder_name, f"table_{i}.xlsx"), index=False)

# 저장과 변환을 한 번에 가능
# csv, json, tsv 지원
# tabula.convert_into("1710.05006.pdf", "output.csv", output_format="csv", pages="all")

# pdfs 라는 폴더가 필요
# tabula.convert_into_by_batch("pdfs", output_format="csv", pages="all")
