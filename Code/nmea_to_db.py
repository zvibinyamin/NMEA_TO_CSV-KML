import csv
import sqlite3
import math
from datetime import datetime
INPUT_FILENAME = "D://dd22.nmea"
with open(INPUT_FILENAME, 'r') as input_file:
    reader = csv.reader(input_file)
    conn = sqlite3.connect('nmea_to_db.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS info')
    #flag will tell us if the GPGGA is good if yes continue to the GPRMC
    flag = 0
    # Create table
    c.execute('''CREATE TABLE info
                     (date text,time text,speed float, latitude text, latitude_direction text, longitude text, longitude_direction text,fix text,horizontal_dilution text,altitude text,direct_of_altitude text,altitude_location text)''')
    # create a csv reader object from the input file (nmea files are basically csv)
    for row in reader:
        # skip all lines that do not start with $GPGGA
        if not row:
            continue
        elif row[0].startswith('$GPGGA') and not row[6]=='0':
            time = row[1]
            latitude = row[2]
            lat_direction = row[3]
            longitude = row[4]
            lon_direction = row[5]
            fix = row[6]
            horizontal = row[7]
            altitude = row[8]
            direct_altitude = row[9]
            altitude_location = row[10]
            flag = 1
        elif row[0].startswith('$GPRMC') and flag==1:
            speed = row[7]
            date = row[9]
            warning = row[2]
            if warning == 'V':
                continue
            date_and_time = datetime.strptime(date + ' ' + time, '%d%m%y %H%M%S.%f');
            date_and_time = date_and_time.strftime('%y-%m-%d %H:%M:%S.%f')[:-3];
            date = date_and_time[0:8];
            time = date_and_time[8:];
            c.execute("INSERT INTO info VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(date,time,speed, latitude, lat_direction, longitude, lon_direction,fix,horizontal,altitude,direct_altitude,altitude_location))
        # Save (commit) the changes
            conn.commit()
            flag=0
        else:
            continue
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
