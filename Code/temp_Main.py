import csv
import sqlite3
import tkinter as tk
from tkinter import filedialog

#flag in order to know when to finish the program
flag=1
while flag!='0':
    print("____________________________________________________________________")
    print()
    print("This is a menu for NMEA convertor")
    print()
    name = input("Please insert your name")
    print()
    print("Hello" ,name , "Please choose the .nmea file")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    #create database
    with open(file_path, 'r') as input_file:
        reader = csv.reader(input_file)
        conn = sqlite3.connect('nmea_to_db.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS info')
        # flag will tell us if the GPGGA is good if yes continue to the GPRMC
        flag = 0
        # Create table
        c.execute('''CREATE TABLE info
                         (date text,time text,speed float, latitude text, latitude_direction text, longitude text, longitude_direction text,fix text,horizontal_dilution text,altitude text,direct_of_altitude text,altitude_location text)''')
        # create a csv reader object from the input file (nmea files are basically csv)
        for row in reader:
            # skip all lines that do not start with $GPGGA
            if not row:
                continue
            elif row[0].startswith('$GPGGA') and not row[6] == '0':
                time = row[1];
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
            elif row[0].startswith('$GPRMC') and flag == 1:
                speed = row[7]
                date = row[9]
                warning = row[2]
                if warning == 'V':
                    continue
                c.execute("INSERT INTO info VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
                date, time, speed, latitude, lat_direction, longitude, lon_direction, fix, horizontal, altitude,
                direct_altitude, altitude_location))
                # Save (commit) the changes
                conn.commit()
                flag = 0
            else:
                continue
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    #end create database


    #ask the user what data he want to see
    print()
    print("What data do you want to see? - for defult leave it blank,if you dont want see something pleae write it in 1 line")
    str_remove = input("date, time, speed, latitude, lat_direction, longitude, lon_direction, fix, horizontal, altitude,direct_altitude, altitude_location")

    #change the data base according to what the user enter
#******************************
    if str_remove!="":
        conn = sqlite3.connect('nmea_to_db.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS info')
        # Create table
        c.execute('''CREATE TABLE info''')
        if "date" in str_remove:
            print("remove date")
        if "time" in str_remove:
            print("remove time")
        if "speed" in str_remove:
            print("remove speed")
        if "latitude" in str_remove:
            print("remove latitude")
        if "lat_direction" in str_remove:
            print("remove lat_direction")
        if "longitude" in str_remove:
            print("remove longitude")
        if "lon_direction" in str_remove:
            print("remove lon direction")
        if "fix" in str_remove:
            print("remove fix")
        if "horizontal" in str_remove:
            print("remove horizontal")
        if "altitude" in str_remove:
            print("remove altitude")
        if "direct_altitude" in str_remove:
            print("remove direct altitude")
        if "altitude_location" in str_remove:
            print("remove altitude location")
#********************************************************
    #ask the user to what he want to convert it
    print()
    print("What would you like to do? ")
    choice = input("If you want to convert to KML please insert 1, if you want to convert to CSV please insert 2")

    # convert db to kml
    if choice=='1':
        InputFile = "C://Users/danie/PycharmProjects/untitled2/Code/nmea_to_db.db"
        OutputFile = "C://Users/danie/PycharmProjects/untitled2/Code/nmea_to_kml.kml"
        connection = sqlite3.connect(InputFile)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM info")

        result = cursor.fetchall()

        f = open(OutputFile, "w")

        # Writing the kml file.
        f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
        f.write("<Document>\n")
        f.write("   <name>" + 'to_kml' + '.kml' + "</name>\n")
        for row in result:
            f.write("   <Placemark>\n")
            f.write("       <name>" + str(row[1]) + "</name>\n")
            f.write("       <description>" + str(row[0]) + "</description>\n")
            day = str(row[0][:2])
            month = str(row[0][2:4])
            year = str(row[0][4:6])
            if (float(year) > 30):
                Date = "19" + year + "-" + month + "-" + day
            elif (float(year) <= 30):
                Date = "20" + year + "-" + month + "-" + day
            hour = str(row[1][:2])
            minute = str(row[1][2:4])
            second = str(row[1][4:6])
            Time = hour + ":" + minute + ":" + second
            f.write("  <TimeStamp>\n" + "<when>" + Date + "T" + Time + "Z</when> \n</TimeStamp>\n")
            f.write("       <Point>\n")
            # print("lat=" + row[3])
            # print("lon=" + row[5])
            lon = str(float(row[5][:3]) + (float(row[5][3:]) / 60))
            lat = str(float(row[3][:2]) + (float(row[3][2:]) / 60))
            #  print(lat)
            #  print(lon)
            a = float(row[5]) / 100
            b = float(row[3]) / 100
            f.write("           <coordinates>" + lon + "," + lat + "," + str(row[9]) + "</coordinates>\n")
            f.write("       </Point>\n")
            f.write("   </Placemark>\n")
        f.write("</Document>\n")
        f.write("</kml>\n")

        cursor.close()
        f.close()
        connection.close()

        #nmea to csv
    if choice == '2':
        INPUT_FILE = "C://Users/danie/PycharmProjects/untitled2/Code/nmea_to_db.db"
        OUTPUT_FILE = "C://Users/danie/PycharmProjects/untitled2/Code/nmea_to_csv.csv"

        file_name = open(OUTPUT_FILE, 'w', newline='')
        c = csv.writer(file_name)

        c.writerow(
            ['Date', 'Time', 'Speed', 'Latitude', 'Lat_direction', 'Longitude', 'Lon_direction', 'Fix', 'Horizontal',
             'Altitude', 'Direct_altitude', 'Altitude_location'])

        connection = sqlite3.connect(INPUT_FILE)

        cursor = connection.cursor()

        cursor.execute('SELECT * FROM info')

        result = cursor.fetchall()

        for r in result:
            c.writerow(r)

        cursor.close()
        file_name.close()
        connection.close()

    flag = input("if you would like quit please press 0")
    print()
