
import sqlite3


connection = sqlite3.connect("C:/Users/sapir/Desktop/nmea_to_db.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM info")

result = cursor.fetchall()

f = open('C:/Users/sapir/Desktop/to_kml.kml', 'w')

#Writing the kml file.
f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
f.write("<Document>\n")
f.write("   <name>" + 'to_kml' + '.kml' +"</name>\n")
for row in result:
    f.write("   <Placemark>\n")
    f.write("       <name>" + str(row[1]) + "</name>\n")
    f.write("       <description>" + str(row[0]) + "</description>\n")
    day = str(row[0][:2])
    month= str(row[0][2:4])
    year = str(row[0][4:6])
    if(float(year)>30):
        Date = "19"+year + "-" + month + "-" + day
    elif (float(year)<=30):
        Date = "20"+year+"-"+month+"-"+day
    hour=str(row[1][:2])
    minute= str(row[1][2:4])
    second=str(row[1][4:6])
    Time=hour+":"+minute+":"+second
    f.write("  <TimeStamp>\n" +"<when>" +Date+"T"+Time+"Z</when> \n</TimeStamp>\n")
    f.write("       <Point>\n")
   # print("lat=" + row[3])
   # print("lon=" + row[5])
    lon=str(float(row[5][:3])+(float(row[5][3:])/60))
    lat = str(float(row[3][:2]) + (float(row[3][2:]) / 60))
  #  print(lat)
  #  print(lon)
    a=float(row[5])/100
    b=float(row[3])/100
    f.write("           <coordinates>" +lon+ "," +lat+ "," + str(row[9]) + "</coordinates>\n")
    f.write("       </Point>\n")
    f.write("   </Placemark>\n")
f.write("</Document>\n")
f.write("</kml>\n")

cursor.close()
f.close()
connection.close()