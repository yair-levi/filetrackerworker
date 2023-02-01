import sqlite3


class FileRepository:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def create_table_if_not_exists(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS files
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name           TEXT    NOT NULL,
                 md5            CHAR(100)     NOT NULL,
                 updated        TIMESTAMP DEFAULT CURRENT_TIMESTAMP);''')

    def add_file(self, file_name, md5):
        sql = '''INSERT INTO files (name, md5)
      VALUES (?, ? )
        '''
        self.conn.execute(sql, (file_name, md5))

    def delete_file_by_name(self, file_name):
        sql = '''DELETE from files where name = ?
           '''
        self.conn.execute(sql, (file_name,))

    def find_by_md5(self, md5):
        sql = '''select name, md5 from files where md5 = ?
           '''
        return self.conn.execute(sql, (md5,)).fetchall()

    def update_md5_by_file_name(self, file_name, md5):
        sql = '''UPDATE files SET md5 = ?
       where name = ?
          '''
        self.conn.execute(sql, (md5, file_name))

    def close_transaction(self):
        self.conn.commit()





