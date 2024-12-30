import mysql.connector as sqltor

con = sqltor.connect(host= 'localhost', user = 'root', password = '12345678', charset = 'utf8')
cur = con.cursor()

cur.execute("DROP DATABASE IF EXISTS file ")
cur.execute("CREATE DATABASE file")
cur.execute("USE file")
query = """CREATE TABLE Student(
    marks int ,
    Rno int PRIMARY KEY)"""
cur.execute(query)
cur.execute("INSERT INTO Student VALUES(80, 1)")
cur.execute("INSERT INTO Student VALUES(90, 2)")
cur.execute("INSERT INTO Student VALUES(85, 3)")
cur.execute("INSERT INTO Student VALUES(70, 4)")
cur.execute("INSERT INTO Student VALUES(100, 5)")
cur.execute("SELECT * FROM Student")

print("Marks, Roll no.")
data = cur.fetchall()
for row in data:
    print(row)
con.commit()

cur.close()
con.close()
