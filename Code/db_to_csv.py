import sqlite3
import csv

file_name= open("to_csv.csv","w")
c=csv.writer(file_name)

c.writerow(['date','time','speed', 'latitude', 'lat_direction', 'longitude', 'lon_direction','fix','horizontal','altitude','direct_altitude','altitude_location'])

connection = sqlite3.connect("nmea_to_db.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM info")

result = cursor.fetchall()
for r in result:
    c.writerow(r)
cursor.execute("SELECT * FROM info")


cursor.close()
file_name.close()
connection.close()
