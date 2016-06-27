
import re
sql = '''
CREATE TABLE `users` (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `username`	TEXT NOT NULL UNIQUE,
    `password`	TEXT NOT NULL,
    `email`	TEXT
)
'''
pattern = re.compile('`(.*)`')
table = pattern.findall(sql)
for i in table:
    print(i)


