import mysql.connector
import pandas as pd 
PhonePe=mysql.connector.connect(host='localhost',
                        database='phonepe',
                        user='root',
                        password='*****')
mycursor = PhonePe.cursor()




### Agregated_Transaction_Table

sql= "CREATE TABLE Aggregated_Transaction (MyIndex INT NOT NULL AUTO_INCREMENT,Payment_Type VARCHAR(50),Total_Transactions BIGINT,Total_Amount BIGINT,Quarter INT,Year INT,State VARCHAR(50),PRIMARY KEY (MyIndex))"
mycursor.execute(sql)
print('Table created successfully.')
PhonePe.commit()
df=pd.read_csv(r'C:\Users\ssjsm\OneDrive\Desktop\Phonepetask\csv\Aggregated_Transactions.csv')
for index, row in df.iterrows():
     quer="INSERT INTO PhonePe.Aggregated_Transaction(Payment_Type,Total_Transactions,Total_Amount,Quarter,Year,State) values(%s,%s,%s,%s,%s,%s)"
     mycursor.execute(quer,(row.Payment_Type,row.Total_Transactions,row.Total_Amount,row.Quarter,row.Year,row.State))
print('DataFrame Inserted successfully.')
PhonePe.commit()
mycursor.close()


#### Aggregated_User_Summary
sql= "CREATE TABLE Aggregated_User_Summary (MyIndex INT NOT NULL AUTO_INCREMENT,State VARCHAR(50),Year INT,Quarter INT,Phonepe_Registered_Users BIGINT,AppOpenings BIGINT,PRIMARY KEY (MyIndex))"
mycursor.execute(sql) 
print('Table created successfully.')
PhonePe.commit()
df=pd.read_csv(r'C:\Users\ssjsm\OneDrive\Desktop\Phonepetask\csv\Aggregated_User_Summary.csv')
for index, row in df.iterrows():
     quer="INSERT INTO PhonePe.Aggregated_User_Summary(State,Year,Quarter,Phonepe_Registered_Users,AppOpenings) values(%s,%s,%s,%s,%s)"
     mycursor.execute(quer,(row.State,row.Year,row.Quarter,row.Phonepe_Registered_Users,row.AppOpenings))
print('DataFrame Inserted successfully.')
PhonePe.commit()
mycursor.close()


####Data_Aggregated_User_Table

sql= "CREATE TABLE Aggregated_User_Table (MyIndex INT NOT NULL AUTO_INCREMENT,Mobile_Model_Name VARCHAR(50),Registered_Users BIGINT,Share_Percentage_of_Mobile_Brand FLOAT,Quarter INT,Year INT,State VARCHAR(50),PRIMARY KEY (MyIndex))"
mycursor.execute(sql)
print('Table created successfully.')
PhonePe.commit()
df=pd.read_csv(r'C:\Users\ssjsm\OneDrive\Desktop\Phonepetask\csv\Aggregated_User_Table.csv')
for index, row in df.iterrows():
     quer="INSERT INTO PhonePe.Aggregated_User_Table(Mobile_Model_Name,Registered_Users,Share_Percentage_of_Mobile_Brand,Quarter,Year,State) values(%s,%s,%s,%s,%s,%s)"
     mycursor.execute(quer,(row.Mobile_Model_Name,row.Registered_Users,row.Share_Percentage_of_Mobile_Brand,row.Quarter,row.Year,row.State))
print('DataFrame Inserted successfully.')
PhonePe.commit()
mycursor.close()


####  Map_Districts_Longitude_Latitude

sql= "CREATE TABLE Map_Districts_GeoLocation( MyIndex INT NOT NULL AUTO_INCREMENT,State VARCHAR(50),District VARCHAR(50),Latitude FLOAT,Longitude FLOAT, PRIMARY KEY (MyIndex))"
mycursor.execute(sql)
print('Table created successfully.')
PhonePe.commit()
df=pd.read_csv(r'C:\Users\ssjsm\OneDrive\Desktop\Phonepetask\csv\Map_Districts_GeoLocation.csv')
for index, row in df.iterrows():
     quer="INSERT INTO PhonePe.Map_Districts_GeoLocation(State,District,Latitude,Longitude) values(%s,%s,%s,%s)"
     mycursor.execute(quer,( row.State, row.District, row.Latitude, row.Longitude))
print('DataFrame Inserted successfully.')
PhonePe.commit()
mycursor.close()



###  Map_Indian_States_Total_Users

sql= "CREATE TABLE Map_IndianStatesTotal_Users(MyIndex INT NOT NULL AUTO_INCREMENT,State VARCHAR(50),Registered_Users BIGINT,PRIMARY KEY (MyIndex))"
mycursor.execute(sql)
print('Table created successfully.')
PhonePe.commit()
df=pd.read_csv(r'C:\Users\ssjsm\OneDrive\Desktop\Phonepetask\csv\Map_Indian_States_Total_Users.csv')
for index, row in df.iterrows():
     quer="INSERT INTO PhonePe.Map_IndianStatesTotal_Users(State,Registered_Users) values(%s,%s)"
     mycursor.execute(quer,(row.State,row.Registered_Users))
print('DataFrame Inserted successfully.')
PhonePe.commit()
mycursor.close()



###  Map_Transaction_Table

sql= "CREATE TABLE Map_Transaction_Table (MyIndex INT NOT NULL AUTO_INCREMENT,Locations VARCHAR(50),Total_Transactions_Locationwise BIGINT,Total_Amount BIGINT,Quarter INT,Year INT,State VARCHAR(50),PRIMARY KEY (MyIndex))"
mycursor.execute(sql)
print('Table created successfully.')
PhonePe.commit()
df=pd.read_csv(r'C:\Users\ssjsm\OneDrive\Desktop\Phonepetask\csv\Map_Transaction_Table.csv')
for index, row in df.iterrows():
     quer="INSERT INTO PhonePe.Map_Transaction_Table(Locations,Total_Transactions_Locationwise,Total_Amount,Quarter,Year,State) values(%s,%s,%s,%s,%s,%s)"
     mycursor.execute(quer,(row.Locations,row.Total_Transactions_Locationwise,row.Total_Amount,row.Quarter,row.Year,row.State))
print('DataFrame Inserted successfully.')
PhonePe.commit()
mycursor.close()



###  State_Geo_Location_Data

sql= "CREATE TABLE State_Geo_Location_Data(MyId INT NOT NULL AUTO_INCREMENT,code VARCHAR(50),Latitude FLOAT,Longitude FLOAT,state VARCHAR(50),PRIMARY KEY (MyId))"
mycursor.execute(sql)
print('Table created successfully.')
PhonePe.commit()
df=pd.read_csv(r'C:\Users\ssjsm\OneDrive\Desktop\Phonepetask\csv\State_Geo_Location_Data.csv')
for index, row in df.iterrows():
     quer="INSERT INTO PhonePe.State_Geo_Location_Data(code,Latitude,Longitude,state) values(%s,%s,%s,%s)"
     mycursor.execute(quer,(row.code,row.Latitude,row.Longitude,row.state))
print('DataFrame Inserted successfully.')
PhonePe.commit()
mycursor.close()


