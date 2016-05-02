#!/usr/bin/python3
# write tkinter as Tkinter to be Python 2.x compatible
from tkinter import *

import os
import os.path
import csv
import sqlite3
import tkinter as tk
from tkinter import filedialog

def DropTable(event):
    c.execute('DROP TABLE IF EXISTS info')
    # Create table
    c.execute('''CREATE TABLE info
                            (fileName text,date date,time time,speed float, latitude text, latitude_direction text, longitude text, longitude_direction text,fix text,horizontal_dilution text,altitude text,direct_of_altitude text,altitude_location text)''')

def show_var(event):
    print("\n----\nfromDate " + fromDate.get())
    print("untilDate " + untilDate.get())
    print("fromTime " + fromTime.get())
    print("untilTime " + untilTime.get())
    print("fromSpeed " + fromSpeed.get())
    print("untilSpeed " + untilSpeed.get())

    print("show date? " + str(show1.get()))
    print("show time? " + str(show2.get()))
    print("show speed? " + str(show3.get()))

def DBToCSV(event):
    print("DB to csv")

    file_name = open(CSV_FILE, 'w', newline='')
    c = csv.writer(file_name)

    c.writerow(
        ['fileName','Date', 'Time', 'Speed', 'Latitude', 'Lat_direction', 'Longitude', 'Lon_direction', 'Fix', 'Horizontal',
         'Altitude', 'Direct_altitude', 'Altitude_location'])

    connection = sqlite3.connect(DB_New_name)

    cursor = connection.cursor()

    # cursor.execute('SELECT * FROM info')

    str = 'SELECT * FROM info where 1==1'
    if (len(fromDate.get()) > 5):
        str += " and date > " + fromDate.get()

    if (len(untilDate.get()) > 5):
        str += " and date < " + untilDate.get()

    if (len(fromTime.get()) > 4):
        str += " and time > " + fromTime.get()

    if (len(untilTime.get()) > 4):
        str += " and time < " + untilTime.get()

    if (len(fromSpeed.get()) > 0):
        str += " and speed > " + fromSpeed.get()

    if (len(untilSpeed.get()) > 0):
        str += " and speed < " + untilSpeed.get()

    print(str)
    cursor.execute(str)

    result = cursor.fetchall()

    for r in result:
        c.writerow(r)

    cursor.close()
    file_name.close()
    connection.close()

def DBToKML(event):
    print("DB to kml")
    connection = sqlite3.connect(DB_New_name)
    cursor = connection.cursor()

    # cursor.execute('SELECT * FROM info')

    str1 = 'SELECT * FROM info where 1==1'
    if (len(fromDate.get()) > 5):
        str1 += " and date > " + fromDate.get()

    if (len(untilDate.get()) > 5):
        str1 += " and date < " + untilDate.get()

    if (len(fromTime.get()) > 4):
        str1 += " and time > " + fromTime.get()

    if (len(untilTime.get()) > 4):
        str1 += " and time < " + untilTime.get()

    if (len(fromSpeed.get()) > 0):
        str1 += " and speed > " + fromSpeed.get()

    if (len(untilSpeed.get()) > 0):
        str1 += " and speed < " + untilSpeed.get()

    print(str1)
    cursor.execute(str1)

    result = cursor.fetchall()
    f = open(KML_File, "w")

    # Writing the kml file.
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
    f.write("<Document>\n")
    f.write("   <name>" + 'to_kml' + '.kml' + "</name>\n")
    num =0
    for row in result:
        num +=1
        rowStr = str(row[1])
        day = str(rowStr[:2])
        month = str(rowStr[2:4])
        year = str(rowStr[4:6])

        if (year.isdigit() & int(year) > 30):
            Date = "19" + year + "-" + month + "-" + day
        else:
            Date = "20" + year + "-" + month + "-" + day

        rowStr = str(row[2])
        hour = str(rowStr[:2])
        minute = str(rowStr[2:4])
        second = str(rowStr[4:6])
        Time = hour + ":" + minute + ":" + second

        f.write("   <Placemark>\n")
        f.write("       <name> point_" + str(num) + "</name>")
        f.write("\n       <description>")
        f.write("\n           <p>Date:" + Date + "</p>")
        f.write("\n           <p>Time:" +  str(Time) + "</p>")
        f.write("\n           <p>Speed: " + str(row[3]) + "</p>")
        f.write("\n           <p>Location: " + str(row[4]) + str(row[5]) + " " + str(row[6]) + str(row[7]) + "</p>")
        f.write("\n           <p>file_name: "+str(row[0])+"</p>")
        f.write("\n       </description>")
        #f.write("       <description>" + str(row[0]) + "</description>\n")

        # Time = row[2]
        # f.write("  <TimeStamp>\n" + "<when>" + str(row[1]) + "T" + str(Time) + "Z</when> \n</TimeStamp>\n")
        f.write("\n       <TimeStamp>" + "\n         <when>" + Date + "T" + str(Time) + "Z</when>\n         </TimeStamp>\n")
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
    with open(file_path, 'r') as DB_name:
        reader = csv.reader(DB_name)
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

def UI_filter(event):
    # c.execute('SELECT * INTO zvika IN \'Backup.db\' FROM info')
    # c.execute('CREATE TABLE copied AS SELECT * FROM info')
    print("exit from this ui")
    button2.destroy()
    button1.destroy()
    button3.destroy()


    conn.close()
    Label(None, text='from date: (like: "1/1/1990")').pack()
    date1_Entry = Entry(None, text='', textvariable=fromDate)
    date1_Entry.pack()


    Label(None, text='until date: (like: "12/12/2020")').pack()
    date2_Entry = Entry(None, text='', textvariable=untilDate)
    date2_Entry.pack()

    Label(None, text='\nfrom hour: (like: "08:03:01")').pack()
    hour1_Entry = Entry(None, text='', textvariable=fromTime)
    hour1_Entry.pack()

    Label(None, text='until hour: (like: "18:59:07")').pack()
    hour2_Entry = Entry(None, text='', textvariable=untilTime)
    hour2_Entry.pack()

    Label(None, text='\nfrom speed: (like: "0.1")').pack()
    Speed1_Entry = Entry(None, text='', textvariable=fromSpeed)
    Speed1_Entry.pack()

    Label(None, text='until speed: (like: "7.45")').pack()
    Speed2_Entry = Entry(None, text='', textvariable=untilSpeed)
    Speed2_Entry.pack()

    Text1 = LabelFrame(None, text="\nshow?")
    Text1.pack()


    Checkbutton1 = Checkbutton(None, text="show date?", variable = show1)
    Checkbutton1.pack()

    Checkbutton2 = Checkbutton(None, text="show time?", variable = show2)
    Checkbutton2.pack()

    Checkbutton3 = Checkbutton(None, text="show speed?", variable = show3)
    Checkbutton3.pack()

    Label(None, text='\n').pack()

    button4 = Button(None, text='save to CSV')
    button4.pack()

    button5 = Button(None, text='save to KML')
    button5.pack()

    button5.bind('<Button>', DBToKML)
    button4.bind('<Button>', DBToCSV)



    Label(None, text='\n').pack()
    button_temp = Button(None, text='show var')
    button_temp.pack()
    button_temp.bind('<Button>', show_var)

DB_name = "nmea_db.db"
DB_New_name = "nmea_db.db"
# DB_New_name = "db_filter.db"
CSV_FILE = "nmea_to_csv.csv"
KML_File = "nmea_to_kml.kml"

if (os.path.isfile(DB_name) == 0):
    # create database
    conn = sqlite3.connect(DB_name)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS info')
    # Create table
    c.execute('''CREATE TABLE info
                        (fileName text,date date,time time,speed float, latitude text, latitude_direction text, longitude text, longitude_direction text,fix text,horizontal_dilution text,altitude text,direct_of_altitude text,altitude_location text)''')
else:
    # create database
    conn = sqlite3.connect(DB_name)
    c = conn.cursor()


button1 = Button(None, text='Upload file')
button1.pack()
button2 = Button(None, text ="Continue to the next step - Data filtering")
button2.pack()

Label1 = Label(None, text='\n').pack()

button3 = Button(None, text='Clear DB')
button3.pack()

fromDate = StringVar()
untilDate = StringVar()
fromTime = StringVar()
untilTime = StringVar()
fromSpeed = StringVar()
untilSpeed = StringVar()
show1 = IntVar()
show2 = IntVar()
show3 = IntVar()

button1.bind('<Button>', UploadFile)
button3.bind('<Button>', DropTable)
button2.bind('<Button>', UI_filter)

# v= StringVar()
# Entry11 = Entry(None, text='', textvariable=v)
# Entry11.pack()

button1.mainloop()
