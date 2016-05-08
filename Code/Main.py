# Software that accepts NMEA files:
# The software saves all data and gives the user an option to filter by file name, dates, times or location
# And view them using google earth or excel (CSV or KML accordingly)

# Instructions:
#  Once the program is running will be two main buttons:
#  1. "Upload file" - button allows you to get your NMEA. (You can use the following sample files: "Examples/nmea files")
#  2. "Continue to the next step - Data filtering" - button allows you to filter data and filtering out files after.
#      On the next screen you can filter files by multiple options.
#      Save the data by clicking on the "save to CSV" or the button "save to KML".



#!/usr/bin/python3
# write tkinter as Tkinter to be Python 2.x compatible
from tkinter import *

import os
import os.path
import csv
import sqlite3
import tkinter as tk
from tkinter import filedialog

# Out of the program
def MyExit(event):
    exit()
# Clears the DataBase
def DropTable(event):
    c.execute('DROP TABLE IF EXISTS info')
    # Create table
    c.execute('''CREATE TABLE info
                            (fileName text,date date,time time,speed float, latitude text, latitude_direction text, longitude text, longitude_direction text,fix text,horizontal_dilution text,altitude text,direct_of_altitude text,altitude_location text,dateint int)''')


# convert DB file to CSV file
def DBToCSV(event):
    print("DB to csv")

    file_name = open(CSV_FILE, 'w', newline='')
    c = csv.writer(file_name)

    c.writerow(
        ['fileName','Date', 'Time', 'Speed', 'Latitude', 'Lat_direction', 'Longitude', 'Lon_direction', 'Fix', 'Horizontal',
         'Altitude', 'Direct_altitude', 'Altitude_location', 'Date_int'])

    connection = sqlite3.connect(DB_name)

    cursor = connection.cursor()

    # cursor.execute('SELECT * FROM info')
    str1 = 'SELECT * FROM info where 1==1'
    if (len(fileNameVar.get()) > 3):
        str1 += " and fileName LIKE  \"%" + fileNameVar.get()+"\""

    if (len(fromDate.get()) == 8):
        str1 += " and dateint > " + fromDate.get()

    if (len(untilDate.get()) == 8):
        str1 += " and dateint < " + untilDate.get()

    if (len(fromTime.get()) > 4):
        str1 += " and time > \'" + fromTime.get() + "\'"

    if (len(untilTime.get()) > 4):
        str1 += " and time < \'" + untilTime.get() + "\'"

    if (len(fromSpeed.get()) > 0):
        str1 += " and speed > " + fromSpeed.get()

    if (len(untilSpeed.get()) > 0):
        str1 += " and speed < " + untilSpeed.get()

    print(str1)
    cursor.execute(str1)

    result = cursor.fetchall()

    for r in result:
        #print(r)
        c.writerow(r)

    cursor.close()
    file_name.close()
    connection.close()

# convert DB file to KML file
def DBToKML(event):
    print("DB to kml")
    connection = sqlite3.connect(DB_name)
    cursor = connection.cursor()

    # cursor.execute('SELECT * FROM info')
    str1 = 'SELECT * FROM info where 1==1'
    if (len(fileNameVar.get()) > 3):
        str1 += " and fileName LIKE  \"%" + fileNameVar.get()+"\""

    if (len(fromDate.get()) == 8):
        str1 += " and dateint > " + fromDate.get()

    if (len(untilDate.get()) == 8):
        str1 += " and dateint < " + untilDate.get()

    if (len(fromTime.get()) > 4):
        str1 += " and time > \'" + fromTime.get() + "\'"

    if (len(untilTime.get()) > 4):
        str1 += " and time < \'" + untilTime.get() + "\'"

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
        month = str(rowStr[3:5])
        year = str(rowStr[6:10])
        Date = year + "-" + month + "-" + day

        Time = str(row[2])

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
        # f.write("  <TimeStamp>\n" + "<when>" + str(row[1]) + "T" + str(Time) + "Z</when> \n</TimeStamp>\n")
        f.write("\n       <TimeStamp>" + "\n         <when>" + Date + "T" + str(Time) + "Z</when>\n         </TimeStamp>\n")
        f.write("       <Point>\n")
        lon = str(float(row[6][:3]) + (float(row[6][3:]) / 60))
        lat = str(float(row[4][:2]) + (float(row[4][2:]) / 60))
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

# Screen bouncing user gives him the option to add a new NMEA to BD
def UploadFile(event):
    print("There will be a code file uploads")

    file_path = filedialog.askopenfilename()
    print("file_path " + file_path)


    if(len(file_path)<4):
        print("You not Select good File")
        return

    if (file_path[-4:] != "nmea"):
        print("2The file most to by NMEA type")
        return

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
                rowStr = str(row[1])
                hour = str(rowStr[:2])
                minute = str(rowStr[2:4])
                second = str(rowStr[4:6])
                time = hour + ":" + minute + ":" + second
                # time = row[1];
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
                # date = row[9]
                rowStr = str(row[9])
                day = str(rowStr[:2])
                month = str(rowStr[2:4])
                year = str(rowStr[4:6])

                if(year.isdigit() & int(year) > 30):
                    year ="19" + year
                else:
                    year = "20" + year

                date = day + "/" + month + "/" + year

                if(len(month)==1 & len(day)==1):
                    date_int = year + "0" + month + "0" + day
                elif(len(month)==1):
                    date_int = year + "0" + month + "" + day
                elif(len(day)==1):
                    date_int = year + "" + month + "0" + day
                else:
                    date_int = year + "" + month + "" + day
                warning = row[2]
                if warning == 'V':
                    continue
                c.execute("INSERT INTO info VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                    file_path, date, time, speed, latitude, lat_direction, longitude, lon_direction, fix, horizontal, altitude,
                    direct_altitude, altitude_location,date_int))
                # Save (commit) the changes
                conn.commit()
                flag = 0
            else:
                continue

# Deletes the UI and adds the buttons of the filter
def UI_filter(event):
    button2.destroy()
    button1.destroy()
    button3.destroy()


    conn.close()

    Label(None, text='Filter by file path: (like:"c:\\\\w1.nmea")').pack()
    fileName_Entry = Entry(None, textvariable=fileNameVar)
    fileName_Entry.pack()

    Label(None, text='\nFilter by from date: (like: "YYYYMMDD")').pack()
    date1_Entry = Entry(None, textvariable=fromDate)
    date1_Entry.pack()

    Label(None, text='Filter by until date: (like: "YYYYMMDD")').pack()
    date2_Entry = Entry(None, textvariable=untilDate)
    date2_Entry.pack()

    Label(None, text='\nFilter by from hour: (like: "HH:MM:SS")').pack()
    hour1_Entry = Entry(None, textvariable=fromTime)
    hour1_Entry.pack()

    Label(None, text='Filter by until hour: (like: "HH:MM:SS")').pack()
    hour2_Entry = Entry(None, textvariable=untilTime)
    hour2_Entry.pack()

    Label(None, text='\nFilter by from speed: (like: "0.1")').pack()
    Speed1_Entry = Entry(None, textvariable=fromSpeed)
    Speed1_Entry.pack()

    Label(None, text='Filter by until speed: (like: "7.45")').pack()
    Speed2_Entry = Entry(None, textvariable=untilSpeed)
    Speed2_Entry.pack()

    Text1 = LabelFrame(None, text="\nshow?")
    Text1.pack()

    Label(None, text='\n').pack()

    button4 = Button(None, text='<< Convert to CSV >>')
    button4.pack()

    Label(None, text='or').pack()

    button5 = Button(None, text='<< Convert to KML  >>')
    button5.pack()

    button5.bind('<Button>', DBToKML)
    button4.bind('<Button>', DBToCSV)

    Label(None, text='\n').pack()
    button6 = Button(None, text='EXIT')
    button6.pack()
    button6.bind('<Button>', MyExit)
    Label1 = Label(None, text='').pack()

DB_name = "nmea_db.db"
CSV_FILE = "nmea_to_csv.csv"
KML_File = "nmea_to_kml.kml"

# Creates a new ID if it does not exist:
if (os.path.isfile(DB_name) == 0):
    # create database
    conn = sqlite3.connect(DB_name)
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS info')
    # Create table
    c.execute('''CREATE TABLE info
                            (fileName text,date date,time time,speed float, latitude text, latitude_direction text, longitude text, longitude_direction text,fix text,horizontal_dilution text,altitude text,direct_of_altitude text,altitude_location text,dateint int)''')
else:
    # create database
    conn = sqlite3.connect(DB_name)
    c = conn.cursor()

# UI:
button1 = Button(None, text='<<   Upload file   >>')
button1.pack()
button3 = Button(None, text='Clear DB')
button3.pack()
Label1 = Label(None, text='                                                                                                          ').pack()
button2 = Button(None, text ="<<  Continue to the next step - Data filtering  >>")
button2.pack()


# The variables retain the values the user has decided to filter:
fromDate = StringVar()
untilDate = StringVar()
fromTime = StringVar()
untilTime = StringVar()
fromSpeed = StringVar()
untilSpeed = StringVar()
fileNameVar = StringVar()
show1 = IntVar()
show2 = IntVar()
show3 = IntVar()


# Add a link to the buttons:
button1.bind('<Button>', UploadFile)
button3.bind('<Button>', DropTable)
button2.bind('<Button>', UI_filter)

button1.mainloop()
