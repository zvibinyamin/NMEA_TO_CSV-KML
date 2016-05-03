import sqlite3
import csv

INPUT_FILE = "C:/Users/sapir/Desktop/nmea_to_db.db"
OUTPUT_FILE = "C:/Users/sapir/Desktop/to_csv.csv"

file_name= open(OUTPUT_FILE,'w', newline='')
c=csv.writer(file_name)

c.writerow(['Date','Time','Speed', 'Latitude', 'Lat_direction', 'Longitude', 'Lon_direction','Fix','Horizontal','Altitude','Direct_altitude','Altitude_location'])

connection = sqlite3.connect(INPUT_FILE)

cursor = connection.cursor()

cursor.execute('SELECT * FROM info')

result = cursor.fetchall()

for r in result:
    c.writerow(r)


cursor.close()
file_name.close()
connection.close()