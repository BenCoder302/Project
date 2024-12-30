import mysql.connector as sqltor

con = sqltor.connect(host= 'localhost', user = 'root', password = '12345678', database = 'file', charset = 'utf8')
cur = con.cursor()

try:
    rollno = int(input("Enter roll no. for searching marks: "))
    cur.execute(f"SELECT marks FROM Student WHERE Rno = {rollno}")
    print(f"Marks of roll no. {rollno} is {cur.fetchall()[0][0]}\n")
except:
    print("Roll no. not found!\n")

con.commit()

cur.close()
con.close()
