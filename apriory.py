#============Apriory========================
import numpy as np
import pandas as pd
from apyori import apriori
import pymysql

con = pymysql.connect(host="localhost", user="root", password="", database="shoptubedb")

store_data=pd.read_csv('groceries1.csv',header=None, encoding='utf-8')
#store_data=pd.read_csv('GROCART1.csv',header=None)
store_data.shape
store_data=store_data.fillna(0)

records=[]
for i in range(0,608):
    records.append([str(store_data.values[i,j]) for j in range(0,30)])

association_rules=apriori(records,min_support=0.13,min_confidence=0.02,min_lift=0.01,min_length=2)
association_rules=list(association_rules)
len = len(association_rules)
print(len)

cur =  con.cursor()
#cur.execute("TRUNCATE TABLE apriori_model")
for i in range(1,len-1):
    #print()
    x = association_rules[i].items
    #print(x)
    x = list(x)


    listToStr = ','.join([str(elem) for elem in x])
    print(listToStr)
    cursor = con.cursor()
    sql = "INSERT INTO apriori_model (productname) VALUES (%s)"
    val = (listToStr)
    cursor.execute(sql, val)
    con.commit()

# cur.execute("select * from groceryname where id= 33")
# products = cur.fetchone()
# print(products[1])
#====================================
