import pymysql

data={}
alldata={}
product = []
with open('groceries.csv') as csv_file:
    product = []

    line_count = 0
    for row in csv_file:
        #print(row)
        splittingdata=row.split(",")
        for im in range(len(splittingdata)):
            data[splittingdata[im]]=splittingdata[im]
            #data['a']=1


con = pymysql.connect(host="localhost", user="root", password="root", database="shoptubedb")
i=0
for key, value in data.items() :
    #print (key)
    i = i+1
    cursor = con.cursor()
    sql = "INSERT INTO groceryname (name) VALUES (%s)"
    val = (key)
    cursor.execute(sql, val)
    con.commit()
print(i)

