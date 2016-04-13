import sqlite3
import csv

file_name= open('C:/Users/sapir/Desktop/to_csv.csv','w', newline='')
c=csv.writer(file_name)

c.writerow(['Date','Time','Speed', 'Latitude', 'Lat_direction', 'Longitude', 'Lon_direction','Fix','Horizontal','Altitude','Direct_altitude','Altitude_location'])

connection = sqlite3.connect('C:/Users/sapir/Desktop/nmea_to_db.db')

cursor = connection.cursor()

cursor.execute('SELECT * FROM info')

result = cursor.fetchall()
print(result)

for r in result:
    print(r)
    c.writerow(r)


cursor.close()
file_name.close()
connection.close()