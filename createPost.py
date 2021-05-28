from flaskext.mysql import MySQL
import pymysql

mysql = MySQL()

class Post:
    def __init__(self, price, apartmentType, quadrature, city):
        self.price = price
        self.apartmentType = apartmentType
        self.quadrature = quadrature
        self.city = city
    
    def createPost(self):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''INSERT INTO post(price, apartmentType, quadrature, city) VALUES (%s, %s, %s, %s)''', (self.price, self.apartmentType, self.quadrature, self.city))
        conn.commit()

    def showPosts(self):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''SELECT * FROM post''')
        rows = cursor.fetchone()       
        if rows is None:
            return
        return [Post(*row) for row in rows]
    
    def filterPrice(price1, price2):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''SELECT price, apartmentType, quadrature, city FROM post WHERE price >= (%s) AND price <= (%s)''', (price1, price2))
        rows = cursor.fetchone()
        if rows is None:
            return
        return [Post(*row) for row in rows]

    def filterType(typeOfApartment):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''SELECT price, apartmentType, quadrature, city FROM post WHERE apartmentType = (%s)''', (typeOfApartment))
        rows = cursor.fetchone()
        if rows is None:
            return
        return [Post(*row) for row in rows]

    def filterQuadrature(quadrature1, quadrature2):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''SELECT price, apartmentType, quadrature, city FROM post WHERE quadrature >= (%s) AND quadrature <= (%s)''', (quadrature1, quadrature2))
        rows = cursor.fetchone()
        if rows is None:
            return
        return [Post(*row) for row in rows]

    def filterCity(cityName):
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('''SELECT price, apartmentType, quadrature, city FROM post WHERE city = (%s)''', (cityName))
        rows = cursor.fetchone()
        if rows is None:
            return
        return [Post(*row) for row in rows]