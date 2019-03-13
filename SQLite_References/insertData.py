import sqlite3

def insert_data(values):
    with sqlite3.connect(r'D:\Documents\sqlite\pythonsqlite.db') as db:
        cursor = db.cursor()
        sql = "insert into Product (Name, Price) values (?,?)"
        cursor.execute(sql,values)
        db.commit()

if __name__ == "__main__":
    #product = ("Espresso",1.5)
    #insert_data(product)
    products = [["Latte",1.35],["Mocha",2.40],["Green Tea",1.20],
                ["Black Tea",1.00],["Americano",1.50]]

    for product in products:
        data=(product[0],product[1])
        insert_data(data)
