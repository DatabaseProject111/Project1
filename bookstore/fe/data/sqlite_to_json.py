import sqlite3
import json

# 连接到SQLite数据库
conn_sqlite = sqlite3.connect('E:\\大二下\\数据库系统\\第一次大作业\\allsturead\\Project_1\\bookstore\\fe\\data\\book_lx.db')
cursor = conn_sqlite.cursor()

# 查询数据并保存为JSON文件
cursor.execute('SELECT * FROM book')
rows = cursor.fetchall()
# 获取列名
column_names = [description[0] for description in cursor.description]

data = []
for row in rows:
    data_row = {}
    for i, column_name in enumerate(column_names):
        if isinstance(row[i], bytes):
            try:
                data_row[column_name] = row[i].decode('utf-8')
            except UnicodeDecodeError:
                data_row[column_name] = row[i].decode('latin-1')
        else:
            data_row[column_name] = row[i]
    data.append(data_row)

with open('book_lx.json', 'w') as f:
    json.dump(data, f, indent=4)

# 关闭连接
conn_sqlite.close()
