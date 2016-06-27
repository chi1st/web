#coding=utf-8
"""
INSERT INTO
`users`(`id`,`username`,`password`,`email`)
VALUES \
    (2,'','',NULL);

UPDATE `users` SET `username`=? WHERE `_rowid_`='2';
UPDATE `users` SET `password`=? WHERE `_rowid_`='2';
UPDATE `users` SET `email`=? WHERE `_rowid_`=/'2';
"""

import sqlite3

# def create(conn):
#     sql_create = '''
#     CREATE TABLE `users` (
#         `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#         `username`	TEXT NOT NULL UNIQUE,
#         `password`	TEXT NOT NULL,
#         `email`	TEXT
#     )
#     '''
#     conn.execute(sql_create)
#     print('创建成功')



def insert(conn, username, password, email):
    sql_insert = '''
    INSERT INTO
        `users`(`username`,`password`,`email`)
    VALUES
        (?, ?, ?);
    '''
    conn.execute(sql_insert, (username, password, email))
    print('插入数据成功')


def select(conn, username):
    sql = '''
    SELECT
        *
    FROM
        users
    WHERE
        username=?
    '''
    # select * from users where username=?
    cursor = conn.execute(sql, (username,))
    all = cursor.fetchall()
    print(all)
    return all


def delete(conn, user_id):
    sql_delete = '''
    DELETE FROM
        users
    WHERE
        id=?
    '''
    conn.execute(sql_delete, (user_id,))


def update(conn, user_id, password, email):
    sql_update = '''
    UPDATE
        `users`
    SET
        `password`=?,
        `email`=?
    WHERE
        `id`=?
    '''
    # UPDATE `users` SET `password` =?,`email` =? WHERE `id` =?
    conn.execute(sql_update, (password, email, user_id))


def messages_by_owner_id(conn, owner_id):
    sql = '''
    SELECT
        *
    FROM
        messages
    WHERE
        `owner_id`=?
    '''
    cursor = conn.execute(sql, (owner_id,))
    all = cursor.fetchall()
    return all


def check_table(conn):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select * from users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        print("%s %s %s" % (row["username"], row["password"], row["role"]))


def create(conn):
    sql_create = '''
    CREATE TABLE `master` (
        `type`	INTEGER NOT NULL DEFAULT 1 CHECK(2) PRIMARY KEY AUTOINCREMENT UNIQUE ,
        `name`	TEXT,
        `rootpage`	INTEGER,
        `sql`	TEXT
    )
    '''
    conn.execute(sql_create)
    print('创建成功')
#INTEGER NOT NULL DEFAULT 1 CHECK(2) PRIMARY KEY AUTOINCREMENT UNIQUE
def decribe_table(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    print(cursor.fetchall())



def main():
    db_path = r'db.sqlite'
    conn = sqlite3.connect(db_path)
    #create(conn)
    print("Opened database successfully")
    #insert(conn, 'sql', '123', '')
    # delete(conn, 2)
    # update(conn, 1, 'new pwd', 'gua@cocode.cc')
    # select(conn, 'gua')
    #msgs = messages_by_owner_id(conn, 2)
    #print(msgs)
    check_table(conn)
    #decribe_table(conn)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
    # print(type((1)))
    # print(type((1,)))
