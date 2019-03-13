import sqlite3

#with sqlite3.connect(r'D:\Documents\sqlite\pythonsqlite2.db') as db:
#    pass

def create_table(db_name,table_name,sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master where name=?",(table_name,))
        result = cursor.fetchall()
        keep_table = True
        if len(result) == 1:
            response = input("the table {0} already exists, do you wish to recreate?".format(table_name))
            if response == "y":
                keep_table = False
                print("The {0} table will be recreated - all existing data will be erased.".format(table_name))
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
            else:
                print("The existing table was kept")
        else:
            keep_table = False
        if not keep_table:
            cursor.execute(sql)
            db.commit()

def create_product_table():
    sql = """create table Product
            (ProductID integer,
            Name text,
            Price real,
            ProductTypeID integer,
            primary key(ProductID)
            foreign key(ProductTypeID) references ProductType(ProductTypeID))"""
    create_table(db_name,"Product",sql)

def create_product_type_table():
    sql = """create table ProductType
            (ProductTypeID integer,
            Description text,
            primary key(ProductTypeID))"""
    create_table(db_name,"ProductType",sql)

if __name__ == '__main__':
    db_name = r'D:\Documents\sqlite\pythonsqlite2.db'
    create_product_table()
    create_product_type_table()
