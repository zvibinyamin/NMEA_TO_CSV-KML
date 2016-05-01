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

def ToCSV(event):
    print("to csv")

def ToKML(event):
    print("to kml")

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


    button5.bind('<Button>', ToKML)
    button4.bind('<Button>', ToCSV)

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
