import mariadb

conn = mariadb.connect(
    user='root',
    password='toor',
    host='127.0.0.1',
    port=3306,
    database='demoexam1'
)