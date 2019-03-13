import sqlite3

with sqlite3.connect(r'D:\Documents\sqlite\pythonsqlite.db') as db:
    pass

def create_table(db_name,sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

if __name__ == '__main__':
    db_name = r'D:\Documents\sqlite\pythonsqlite.db'
    sql = """create table Product
            (ProductID integer,
            name text,
            Price real,
            primary key(ProductID))"""

    create_table(db_name,sql)
