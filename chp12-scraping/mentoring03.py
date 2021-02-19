# pip install PySide2
# pip install ghost.py --pre
# QtWebkit 이 없다는 오류를 발생한다.
# QtWebkit 은 deprecated 됐고, 그 이후로 ghost.py 는 업데이트가 되지 않아 사용이 불가능하다.

# from ghost import Ghost
#
# ghost = Ghost()
# with ghost.start() as session:
#     page, extra_resources = session.open('http://python.org')
#
#     print(page)
#     print(page.url)
#     print(page.headers)
#     print(page.http_status)
#     print(page.content)
#
#     print(extra_resources)
#
#     for r in extra_resources:
#         print(r.url)
