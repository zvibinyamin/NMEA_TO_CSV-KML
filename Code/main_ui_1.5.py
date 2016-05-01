#!/usr/bin/python3
# write tkinter as Tkinter to be Python 2.x compatible
from tkinter import *

import csv
import sqlite3
import tkinter as tk
from tkinter import filedialog

def DropTable(event):
    c.execute('DROP TABLE IF EXISTS info')
    # Create table
    c.execute('''CREATE TABLE info
                            (fileName text,date text,time text,speed float, latitude text, latitude_direction text, longitude text, longitude_direction text,fix text,horizontal_dilution text,altitude text,direct_of_altitude text,altitude_location text)''')

def DBToCSV(event):
    print("DB to csv")
    INPUT_FILE = "nmea_to_db.db"
    OUTPUT_FILE = "nmea_to_csv.csv"

    file_name = open(OUTPUT_FILE, 'w', newline='')
    c = csv.writer(file_name)

    c.writerow(
        ['fileName','Date', 'Time', 'Speed', 'Latitude', 'Lat_direction', 'Longitude', 'Lon_direction', 'Fix', 'Horizontal',
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

def DBToKML(event):
    print("DB to kml")
    InputFile = "nmea_to_db.db"
    OutputFile = "nmea_to_kml.kml"
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
        day = str(row[1][:2])
        month = str(row[1][2:4])
        year = str(row[1][4:6])

        if (year.isdigit() & int(year) > 30):
            Date = "19" + year + "-" + month + "-" + day
        else:
            Date = "20" + year + "-" + month + "-" + day

        hour = str(row[2][:2])
        minute = str(row[2][2:4])
        second = str(row[2][4:6])
        Time = hour + ":" + minute + ":" + second
        f.write("  <TimeStamp>\n" + "<when>" + Date + "T" + Time + "Z</when> \n</TimeStamp>\n")
        f.write("       <Point>\n")
        # print("lat=" + row[3])
        # print("lon=" + row[5])
        lon = str(float(row[6][:3]) + (float(row[6][3:]) / 60))
        lat = str(float(row[4][:2]) + (float(row[4][2:]) / 60))
        #  print(lat)
        #  print(lon)
        a = float(row[6]) / 100
        b = float(row[4]) / 100
        f.write("           <coordinates>" + lon + "," + lat + "," + str(row[9]) + "</coordinates>\n")
        f.write("       </Point>\n")
        f.write("   </Placemark>\n")
    f.write("</Document>\n")
    f.write("</kml>\n")

    cursor.close()
    f.close()
    connection.close()


def UploadFile(event):
    print("There will be a code file uploads")

    file_path = filedialog.askopenfilename()

    # create database
    with open(file_path, 'r') as input_file:
        reader = csv.reader(input_file)
        # flag will tell us if the GPGGA is good if yes continue to the GPRMC
        flag = 0
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
                c.execute("INSERT INTO info VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                    file_path, date, time, speed, latitude, lat_direction, longitude, lon_direction, fix, horizontal, altitude,
                    direct_altitude, altitude_location))
                # Save (commit) the changes
                conn.commit()
                flag = 0
            else:
                continue


def filteringFiles(event):
    print("exit from this ui")
    button2.destroy()
    button1.destroy()

    conn.close()

    date1_button = Button(None, text='from date: (like: "1/1/1990")')
    date1_button.pack()
    date1_Entry = Entry(None, text='')
    date1_Entry.pack()

    date2_button = Button(None, text='until date: (like: "12/12/2020")')
    date2_button.pack()
    date2_Entry = Entry(None, text='')
    date2_Entry.pack()

    hour1_button = Button(None, text='from hour: (like: "08:03:01")')
    hour1_button.pack()
    hour1_Entry = Entry(None, text='')
    hour1_Entry.pack()

    hour2_button = Button(None, text='until hour: (like: "18:59:07")')
    hour2_button.pack()
    hour2_Entry = Entry(None, text='')
    hour2_Entry.pack()

    Text1 = LabelFrame(None, text="show?")
    Text1.pack()

    Checkbutton1 = Checkbutton(None, text="show date?")
    Checkbutton1.pack()
    Checkbutton2 = Checkbutton(None, text="show time?")
    Checkbutton2.pack()
    Checkbutton3 = Checkbutton(None, text="show speed?")
    Checkbutton3.pack()
    Checkbutton4 = Checkbutton(None, text="show latitude?")
    Checkbutton4.pack()
    Checkbutton5 = Checkbutton(None, text="show lat_direction?")
    Checkbutton5.pack()

    button4 = Button(None, text='save to CSV')
    button4.pack()

    button5 = Button(None, text='save to KML')
    button5.pack()


    button5.bind('<Button>', DBToKML)
    button4.bind('<Button>', DBToCSV)

# create database
conn = sqlite3.connect('nmea_to_db.db')
c = conn.cursor()

button3 = Button(None, text='Drop Table')
button3.pack()

button1 = Button(None, text='Upload file')
button1.pack()


button2 = Button(None, text ="Go to step filtering files")
button2.pack()


button1.bind('<Button>', UploadFile)
button3.bind('<Button>', DropTable)
button2.bind('<Button>', filteringFiles)
button1.mainloop()
