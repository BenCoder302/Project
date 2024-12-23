import mysql.connector as sqltor

con = sqltor.connect(host= 'localhost', user = 'root', password = '12345678', database = 'file', charset = 'utf8')
cur = con.cursor()

st = input("Enter new marks of student: ")
r = int(input("Enter the roll no. for which you want to update the stream: "))

query = "UPDATE Student SET marks = '{}' where Rno = '{}'".format(st, r)
cur.execute(query)

con.commit()
print("Record Updated Successfully...")
