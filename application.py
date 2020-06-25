import sys
import datetime
import random
import time

# PYQT MODULES
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# MONGODB CONNECTOR
from pymongo import MongoClient

# ML LIBRARIES
import numpy as np
import scipy as sp
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

# CSV CREATION
import csv

# MAP REDUCE
from bson.code import Code

# Declare global variables for entire program
global client, db, airports , flights, fontmain, font

# Creating connection with MongoDB
client=MongoClient()
db=client.aviation
airports=db.airports
airlines=db.airlines
flights=db.flights

fontmain = QFont() 
font = QFont() 
fontmain.setPointSize(20)
font.setPointSize(12)

# HOME PAGE
class Home(QWidget):
    def __init__(self,parent=None):    #Constructor of the class
        super(Home,self).__init__(parent)
        self.InitWindow()    #Calling the InitWindow Funtion to initialize elements of page

    def InitWindow(self):

        self.mainlabel=QLabel("FLIGHT\nDELAY\nANALYSIS",self)    # To create a label
        self.mainlabel.move(75,100)    # To position arguments--> left,top
        self.mainlabel.resize(500,150)    # To resize --> width,height
        self.mainlabel.setFont(fontmain)    # To set font class as fontmain
        self.mainlabel.setStyleSheet("color:white;")    # to set font color

        self.crudButton=QPushButton("CRUD \nOperations",self)   # Create a push button and name it "Crud Operation"
        self.crudButton.move(550,100)
        self.crudButton.resize(150,150)
        self.crudButton.setFont(font)

        self.mlButton=QPushButton("Machine \nLearning",self)
        self.mlButton.move(775,100)
        self.mlButton.resize(150,150)
        self.mlButton.setFont(font)

        self.visButton=QPushButton("Visualization \nReports",self)
        self.visButton.move(550,325)
        self.visButton.resize(150,150)
        self.visButton.setFont(font)
        self.visButton.setShortcut("Ctrl+V")

        self.mpButton=QPushButton("Map Reduce \nOperations",self)
        self.mpButton.move(775,325)
        self.mpButton.resize(150,150)
        self.mpButton.setFont(font)

class CRUD1(QWidget):
    def __init__(self,parent=None):
        super(CRUD1,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("CRUD\nOPERATIONS",self)   
        self.mainlabel.move(75,100)    
        self.mainlabel.resize(500,100)   
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.i1Btn=QPushButton("Insert to\nDatabase",self)
        self.i1Btn.move(308,100)
        self.i1Btn.resize(150,150)
        self.i1Btn.setFont(font)

        self.r2Btn=QPushButton("View Airports\nand Airlines",self)
        self.r2Btn.move(542,100)
        self.r2Btn.resize(150,150)
        self.r2Btn.setFont(font)

        self.r3Btn=QPushButton("Find Flights\nby Source\nand Destination",self)
        self.r3Btn.move(75,325)
        self.r3Btn.resize(150,150)
        self.r3Btn.setFont(font)

        self.r4Btn=QPushButton("Airline\nStatistics",self)
        self.r4Btn.move(308,325)
        self.r4Btn.resize(150,150)
        self.r4Btn.setFont(font)

        self.r1Btn=QPushButton("View Flight\nDetails by\nFlight Number\nand Date",self)
        self.r1Btn.move(775,100)
        self.r1Btn.resize(150,150)
        self.r1Btn.setFont(font)

        self.d1Btn=QPushButton("Delete Flights\nby Airline on\nSpecific Date",self)
        self.d1Btn.move(542,325)
        self.d1Btn.resize(150,150)
        self.d1Btn.setFont(font)

        self.d2Btn=QPushButton("Delete Flights\nby Delay",self)
        self.d2Btn.move(775,325)
        self.d2Btn.resize(150,150)
        self.d2Btn.setFont(font)    

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)

class Insert(QWidget):
    def __init__(self,parent=None):
        super(Insert,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("Insert into Database",self)
        self.mainlabel.move(375,20)
        self.mainlabel.resize(250,40)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.airlinelabel=QLabel("Airline",self)
        self.airlinelabel.move(75,80)
        self.airlinelabel.resize(100,30)
        self.airlinelabel.setFont(font)
        self.airlinelabel.setStyleSheet("color:white;")

        self.airline=QComboBox(self)     # Creating dropdown
        self.airline.move(145,80)
        self.airline.resize(220,30)
        self.airline.setFont(font)

        self.airline.addItem("United Air Lines Inc.")
        self.airline.addItem("American Airlines Inc.")
        self.airline.addItem("US Airways Inc.")
        self.airline.addItem("Frontier Airlines Inc.")
        self.airline.addItem("JetBlue Airways")
        self.airline.addItem("Skywest Airlines Inc.")
        self.airline.addItem("Alaska Airlines Inc.")
        self.airline.addItem("Spirit Air Lines")
        self.airline.addItem("Southwest Airlines Co.")
        self.airline.addItem("Delta Air Lines Inc.")
        self.airline.addItem("Atlantic Southeast Airlines")
        self.airline.addItem("Hawaiian Airlines Inc.")
        self.airline.addItem("American Eagle Airlines Inc.")
        self.airline.addItem("Virgin America")
        
        self.flightlabel=QLabel("Fl Number",self)
        self.flightlabel.move(405,80)
        self.flightlabel.resize(100,30)
        self.flightlabel.setFont(font)
        self.flightlabel.setStyleSheet("color:white;")

        self.flightbox=QLineEdit(self)    # Creating input box
        self.flightbox.move(500,80)
        self.flightbox.resize(150,30)
        self.flightbox.setFont(font)

        self.taillabel=QLabel("Tail Number",self)
        self.taillabel.move(680,80)
        self.taillabel.resize(100,30)
        self.taillabel.setFont(font)
        self.taillabel.setStyleSheet("color:white;")

        self.tailbox=QLineEdit(self)
        self.tailbox.move(775,80)
        self.tailbox.resize(150,30)
        self.tailbox.setFont(font)

        self.sourcelabel=QLabel("Source",self)
        self.sourcelabel.move(75,145)
        self.sourcelabel.resize(100,30)
        self.sourcelabel.setFont(font)
        self.sourcelabel.setStyleSheet("color:white;")

        self.source=QComboBox(self)
        self.source.move(170,145)
        self.source.resize(450,30)
        self.source.setFont(font)

        self.source.addItem("Hartsfield-Jackson Atlanta International Airport, Atlanta")
        self.source.addItem("Gen. Edward Lawrence Logan International Airport, Boston")
        self.source.addItem("Charlotte Douglas International Airport, Charlotte")
        self.source.addItem("Denver International Airport, Denver")
        self.source.addItem("Dallas/Fort Worth International Airport, Dallas-Fort Worth")
        self.source.addItem("Detroit Metropolitan Airport, Detroit")
        self.source.addItem("Newark Liberty International Airport, Newark")
        self.source.addItem("George Bush Intercontinental Airport, Houston")
        self.source.addItem("John F. Kennedy International Airport, New York")
        self.source.addItem("McCarran International Airport, Las Vegas")
        self.source.addItem("Los Angeles International Airport, Los Angeles")
        self.source.addItem("LaGuardia Airport, New York")
        self.source.addItem("Orlando International Airport, Orlando")
        self.source.addItem("Miami International Airport, Miami")
        self.source.addItem("Minneapolis-Saint Paul International Airport, Minneapolis")
        self.source.addItem("Chicago O'Hare International Airport, Chicago")
        self.source.addItem("Philadelphia International Airport, Philadelphia")
        self.source.addItem("Phoenix Sky Harbor International Airport, Phoenix")
        self.source.addItem("Seattle-Tacoma International Airport, Seattle")
        self.source.addItem("San Francisco International Airport, San Francisco")
        
        self.destinationlabel=QLabel("Destination",self)
        self.destinationlabel.move(75,210)
        self.destinationlabel.resize(100,30)
        self.destinationlabel.setFont(font)
        self.destinationlabel.setStyleSheet("color:white;")

        self.destination=QComboBox(self)
        self.destination.move(170,210)
        self.destination.resize(450,30)
        self.destination.setFont(font)

        self.destination.addItem("Hartsfield-Jackson Atlanta International Airport, Atlanta")
        self.destination.addItem("Gen. Edward Lawrence Logan International Airport, Boston")
        self.destination.addItem("Charlotte Douglas International Airport, Charlotte")
        self.destination.addItem("Denver International Airport, Denver")
        self.destination.addItem("Dallas/Fort Worth International Airport, Dallas-Fort Worth")
        self.destination.addItem("Detroit Metropolitan Airport, Detroit")
        self.destination.addItem("Newark Liberty International Airport, Newark")
        self.destination.addItem("George Bush Intercontinental Airport, Houston")
        self.destination.addItem("John F. Kennedy International Airport, New York")
        self.destination.addItem("McCarran International Airport, Las Vegas")
        self.destination.addItem("Los Angeles International Airport, Los Angeles")
        self.destination.addItem("LaGuardia Airport, New York")
        self.destination.addItem("Orlando International Airport, Orlando")
        self.destination.addItem("Miami International Airport, Miami")
        self.destination.addItem("Minneapolis-Saint Paul International Airport, Minneapolis")
        self.destination.addItem("Chicago O'Hare International Airport, Chicago")
        self.destination.addItem("Philadelphia International Airport, Philadelphia")
        self.destination.addItem("Phoenix Sky Harbor International Airport, Phoenix")
        self.destination.addItem("Seattle-Tacoma International Airport, Seattle")
        self.destination.addItem("San Francisco International Airport, San Francisco")

        self.distancelabel=QLabel("Distance",self)
        self.distancelabel.move(680,145)
        self.distancelabel.resize(200,30)
        self.distancelabel.setFont(font)
        self.distancelabel.setStyleSheet("color:white;")
        
        self.distance=QSpinBox(self)    # Creating an input type for numbers
        self.distance.move(805,145)
        self.distance.resize(120,30)
        self.distance.setRange(0,10000)
        self.distance.setFont(font)

        self.divertedlabel=QLabel("Diverted",self)
        self.divertedlabel.move(680,210)
        self.divertedlabel.resize(200,30)
        self.divertedlabel.setFont(font)
        self.divertedlabel.setStyleSheet("color:white;")

        self.diverted=QRadioButton(self)    # Creating a input type of radio button
        self.diverted.move(760,210)
        self.diverted.resize(15,30)
        self.diverted.setFont(font)
        
        self.cancelledlabel=QLabel("Cancelled",self)
        self.cancelledlabel.move(825,210)
        self.cancelledlabel.resize(200,30)
        self.cancelledlabel.setFont(font)
        self.cancelledlabel.setStyleSheet("color:white;")

        self.cancelled=QRadioButton(self)
        self.cancelled.move(915,210)
        self.cancelled.resize(15,30)
        self.cancelled.setFont(font)

        self.schDeptlabel=QLabel("Scheduled Departure",self)
        self.schDeptlabel.move(75,275)
        self.schDeptlabel.setFont(font)
        self.schDeptlabel.setStyleSheet("color:white;")

        self.schDept=QDateTimeEdit(self)    # Creating a date and time input box
        self.schDept.move(245,275)
        self.schDept.resize(200,30)
        self.schDept.setFont(font)
        self.schDept.setDate(QDate(2015,1,1))   # Set default date in dateEdit box

        self.schArrlabel=QLabel("Schedued Arrival",self)
        self.schArrlabel.move(555,275)
        self.schArrlabel.setFont(font)
        self.schArrlabel.setStyleSheet("color:white;")

        self.schArr=QDateTimeEdit(self)
        self.schArr.move(725,275)
        self.schArr.resize(200,30)
        self.schArr.setFont(font)
        self.schArr.setDate(QDate(2015,1,1))

        self.deptlabel=QLabel("Departure",self)
        self.deptlabel.move(75,340)
        self.deptlabel.setFont(font)
        self.deptlabel.setStyleSheet("color:white;")

        self.dept=QDateTimeEdit(self)
        self.dept.move(245,340)
        self.dept.resize(200,30)
        self.dept.setFont(font)
        self.dept.setDate(QDate(2015,1,1))
        
        self.arrlabel=QLabel("Arrival ",self)
        self.arrlabel.move(555,340)
        self.arrlabel.setFont(font)
        self.arrlabel.setStyleSheet("color:white;")

        self.arr=QDateTimeEdit(self)
        self.arr.move(725,340)
        self.arr.resize(200,30)
        self.arr.setFont(font)
        self.arr.setDate(QDate(2015,1,1))

        self.wheelsOfflabel=QLabel("Wheels Off",self)
        self.wheelsOfflabel.move(75,405)
        self.wheelsOfflabel.setFont(font)
        self.wheelsOfflabel.setStyleSheet("color:white;")

        self.wheelsOff=QDateTimeEdit(self)
        self.wheelsOff.move(245,405)
        self.wheelsOff.resize(200,30)
        self.wheelsOff.setFont(font)
        self.wheelsOff.setDate(QDate(2015,1,1))

        self.wheelsOnlabel=QLabel("Wheels On",self)
        self.wheelsOnlabel.move(555,405)
        self.wheelsOnlabel.setFont(font)
        self.wheelsOnlabel.setStyleSheet("color:white;")

        self.wheelsOn=QDateTimeEdit(self)
        self.wheelsOn.move(725,405)
        self.wheelsOn.resize(200,30)
        self.wheelsOn.setFont(font)
        self.wheelsOn.setDate(QDate(2015,1,1))

        self.insertButton=QPushButton("Insert to Database",self)
        self.insertButton.move(350,490)
        self.insertButton.resize(300,30)
        self.insertButton.setFont(font)
        self.insertButton.clicked.connect(self.Inserter)   # Connect with insertData function. Can be declared here because calls function within a class

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)
    

    def timeFormat(self,time):   # Time format converter
        return int("%02d"%time.hour+"%02d"%time.minute)
    
    def timeDiff(self,dt1,dt2):   #Date time difference 
        diff=dt2-dt1
        return diff

    def Inserter(self):   # Function to insert data into database
        
        date=self.schDept.date().toPyDate()   # Get date of flight from the dateTimeEdit of schDept
        flight=self.flightbox.text()   # Get Flight Number
        if flight=='':   # In case left empty
            flight=0000   # Important to initialize because we insert int value and int of NULL value gives error
        tail=self.tailbox.text()   # Get tail number which is a string
        distance=self.distance.value()   # Get distance value from spinbox
        cancelled=int(self.cancelled.isChecked())   # 0--> if unchecked and 1 otherwise
        diverted=int(self.diverted.isChecked())

        schDept=self.timeFormat(self.schDept.time().toPyTime())   # Converting to time format as required by database i.e 01:00:00 becomes 0100
        schArr=self.timeFormat(self.schArr.time().toPyTime())
        scheduled=int(self.timeDiff(self.schDept.dateTime().toPyDateTime(),self.schArr.dateTime().toPyDateTime()).total_seconds()/60)   #Scheduled_time=scheduled_arrival-scheduled_departure

        if cancelled==1:   # In case of cancellation, these parameters become NULL
            dept=''
            wheelsOff=''
            arr=''
            wheelsOn=''
            d_delay==''
            a_delay=''
            elapsed==''
            air=''
        else:
        
            dept=self.timeFormat(self.dept.time().toPyTime()) # Argument is PyTime conversion of time part of dateTime Edit
            wheelsOff=self.timeFormat(self.wheelsOff.time().toPyTime())

            d_delay=int(self.timeDiff(self.schDept.dateTime().toPyDateTime(),self.dept.dateTime().toPyDateTime()).total_seconds()/60)   # Calculate departure_delay=departure-scheduled_departure

            
            arr=self.timeFormat(self.arr.time().toPyTime())
            wheelsOn=self.timeFormat(self.wheelsOn.time().toPyTime())

            a_delay=int(self.timeDiff(self.schArr.dateTime().toPyDateTime(),self.arr.dateTime().toPyDateTime()).total_seconds()/60)   #Arrival_delay=arrival-scheduled_arival

            taxi_out=int(self.timeDiff(self.dept.dateTime().toPyDateTime(),self.wheelsOff.dateTime().toPyDateTime()).total_seconds()/60)   # Taxi_out=wheels_off-departure

            taxi_in=int(self.timeDiff(self.wheelsOn.dateTime().toPyDateTime(),self.arr.dateTime().toPyDateTime()).total_seconds()/60)   #taxi_in=arrival-wheels_on

            elapsed=int(self.timeDiff(self.dept.dateTime().toPyDateTime(),self.arr.dateTime().toPyDateTime()).total_seconds()/60)   # Time taken by flight, elapsed_time=arrival-departure
        
            air=elapsed-taxi_in-taxi_out # Actual air time

        src=self.source.currentText().split(",")  # Split combo-box value as airport, city
        srcq=db.airports.find({'AIRPORT': src[0]})   # Find airport record from airports collection
        source=srcq[0]['IATA_CODE']   # Find IATA_CODE of airport

        dest=self.destination.currentText().split(",")
        destq=db.airports.find({'AIRPORT': dest[0]})
        destination=destq[0]['IATA_CODE']

        airlq=db.airlines.find({'AIRLINE': self.airline.currentText()})
        airline=airlq[0]['IATA_CODE']
        
        # Create the document
        flights_1={'YEAR' : date.year, 'MONTH' : date.month, 'DAY' : date.day, 'DAY_OF_WEEK' : date.weekday()+1,'AIRLINE' : airline,'FLIGHT_NUMBER' : int(flight),'TAIL_NUMBER' : '',
           'ORIGIN_AIRPORT' : source, 'DESTINATION_AIRPORT' : destination,
           'SCHEDULED_DEPARTURE' : schDept, 'DEPARTURE_TIME' : dept, 'DEPARTURE_DELAY' : d_delay,'TAXI_OUT' : taxi_out, 'WHEELS_OFF' : wheelsOff,
           'SCHEDULED_TIME' : scheduled, 'ELAPSED_TIME' : elapsed, 'AIR_TIME' : air, 'DISTANCE' : distance, 'WHEELS_ON' : wheelsOn, 'TAXI_IN' : taxi_in,
           'SCHEDULED_ARRIVAL' : schArr, 'ARRIVAL_TIME' : arr, 'ARRIVAL_DELAY' : a_delay, 'DIVERTED' : diverted, 'CANCELLED' : cancelled
          }
        insertone = flights.insert_one(flights_1)   # Execute insertOne query

class R1(QWidget):
    def __init__(self,parent=None):
        super(R1,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("View Flight\nDetails by\nFlight Number\nand Date",self)
        self.mainlabel.move(75,80)
        self.mainlabel.resize(250,130)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.mainarea=QTextEdit(self)
        self.mainarea.move(325,80)
        self.mainarea.resize(600,400)
        self.mainarea.setFont(font)

        self.flightlabel=QLabel("Fl Number",self)
        self.flightlabel.move(75,260)
        self.flightlabel.resize(175,30)
        self.flightlabel.setFont(font)
        self.flightlabel.setStyleSheet("color:white;")

        self.flightbox=QLineEdit(self)
        self.flightbox.move(75,290)
        self.flightbox.resize(175,30)
        self.flightbox.setFont(font)

        self.datelabel=QLabel("Date",self)
        self.datelabel.move(75,350)
        self.datelabel.resize(175,30)
        self.datelabel.setFont(font)
        self.datelabel.setStyleSheet("color:white;")

        self.date=QDateEdit(self)
        self.date.move(75,380)
        self.date.resize(175,30)
        self.date.setFont(font)
        self.date.setDate(QDate(2015,1,1))

        self.submitButton=QPushButton("View",self)
        self.submitButton.move(75,450)
        self.submitButton.resize(175,30)
        self.submitButton.setFont(font)
        self.submitButton.clicked.connect(self.Finder)

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)
    
    def Finder(self):
        
        self.mainarea.clear()   # Clear display area
        self.cursor=QTextCursor(self.mainarea.document())   # Create cursor object forr display area

        flight=self.flightbox.text()   # Get flight number
        if flight=='':
            flight=0
        date=self.date.date().toPyDate()   # Get date from dateEdit

        flq=db.flights.find({"FLIGHT_NUMBER": int(flight), "DAY" : date.day,"MONTH" : date.month, "YEAR" : date.year})
        
        for record in flq:
            srcq=db.airports.find({'IATA_CODE': record['ORIGIN_AIRPORT']})
            source=srcq[0]['AIRPORT']+", "+srcq[0]['CITY']

            destq=db.airports.find({'IATA_CODE': record['DESTINATION_AIRPORT']})
            destination=destq[0]['AIRPORT']+", "+destq[0]['CITY']

            self.cursor.insertText("\n\nSource :\t\t{0}\nDestination :\t{1}\nSch Departure :\t{2}\nSch Arrival :\t{3}".format( source ,destination,record['SCHEDULED_DEPARTURE'],record['SCHEDULED_ARRIVAL']))


class R2(QWidget):
    def __init__(self,parent=None):
        super(R2,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("View Airports\nand Airlines",self)
        self.mainlabel.move(75,80)
        self.mainlabel.resize(250,80)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.mainarea=QPlainTextEdit(self)
        self.mainarea.move(325,80)
        self.mainarea.resize(600,400)
        self.mainarea.setFont(font)

        self.select=QComboBox(self)
        self.select.move(75,230)
        self.select.resize(175,30)
        self.select.addItem("Airports")
        self.select.addItem("Airlines")
        self.select.setFont(font)

        self.submitButton=QPushButton("View",self)
        self.submitButton.move(75,320)
        self.submitButton.resize(175,30)
        self.submitButton.setFont(font)
        self.submitButton.clicked.connect(self.Finder)

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)
    
    def Finder(self):
        
        select=self.select.currentText()
        
        self.mainarea.clear()
        self.cursor=QTextCursor(self.mainarea.document())

        if select=='Airports':
            slq=db.airports.find()
            for record in slq:
                self.cursor.insertText('{0}\n'.format(record['AIRPORT']))
        else:
            slq=db.airlines.find()
            for record in slq:
                self.cursor.insertText('{0}\n'.format(record['AIRLINE']))


class R3(QWidget):
    def __init__(self,parent=None):
        super(R3,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("Find Flights by Source and Destination",self)
        self.mainlabel.move(75,80)
        self.mainlabel.resize(470,40)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.mainarea=QTextEdit(self)
        self.mainarea.move(600,80)
        self.mainarea.resize(325,340)
        self.mainarea.setFont(font)

        self.sourcelabel=QLabel("Source",self)
        self.sourcelabel.move(75,130)
        self.sourcelabel.resize(100,30)
        self.sourcelabel.setFont(font)
        self.sourcelabel.setStyleSheet("color:white;")

        self.source=QComboBox(self)
        self.source.move(75,160)
        self.source.resize(450,30)
        self.source.setFont(font)

        self.source.addItem("Hartsfield-Jackson Atlanta International Airport, Atlanta")
        self.source.addItem("Gen. Edward Lawrence Logan International Airport, Boston")
        self.source.addItem("Charlotte Douglas International Airport, Charlotte")
        self.source.addItem("Denver International Airport, Denver")
        self.source.addItem("Dallas/Fort Worth International Airport, Dallas-Fort Worth")
        self.source.addItem("Detroit Metropolitan Airport, Detroit")
        self.source.addItem("Newark Liberty International Airport, Newark")
        self.source.addItem("George Bush Intercontinental Airport, Houston")
        self.source.addItem("John F. Kennedy International Airport, New York")
        self.source.addItem("McCarran International Airport, Las Vegas")
        self.source.addItem("Los Angeles International Airport, Los Angeles")
        self.source.addItem("LaGuardia Airport, New York")
        self.source.addItem("Orlando International Airport, Orlando")
        self.source.addItem("Miami International Airport, Miami")
        self.source.addItem("Minneapolis-Saint Paul International Airport, Minneapolis")
        self.source.addItem("Chicago O'Hare International Airport, Chicago")
        self.source.addItem("Philadelphia International Airport, Philadelphia")
        self.source.addItem("Phoenix Sky Harbor International Airport, Phoenix")
        self.source.addItem("Seattle-Tacoma International Airport, Seattle")
        self.source.addItem("San Francisco International Airport, San Francisco")

        self.destinationlabel=QLabel("Destination",self)
        self.destinationlabel.move(75,220)
        self.destinationlabel.resize(100,30)
        self.destinationlabel.setFont(font)
        self.destinationlabel.setStyleSheet("color:white;")

        self.destination=QComboBox(self)
        self.destination.move(75,250)
        self.destination.resize(450,30)
        self.destination.setFont(font)

        self.destination.addItem("Hartsfield-Jackson Atlanta International Airport, Atlanta")
        self.destination.addItem("Gen. Edward Lawrence Logan International Airport, Boston")
        self.destination.addItem("Charlotte Douglas International Airport, Charlotte")
        self.destination.addItem("Denver International Airport, Denver")
        self.destination.addItem("Dallas/Fort Worth International Airport, Dallas-Fort Worth")
        self.destination.addItem("Detroit Metropolitan Airport, Detroit")
        self.destination.addItem("Newark Liberty International Airport, Newark")
        self.destination.addItem("George Bush Intercontinental Airport, Houston")
        self.destination.addItem("John F. Kennedy International Airport, New York")
        self.destination.addItem("McCarran International Airport, Las Vegas")
        self.destination.addItem("Los Angeles International Airport, Los Angeles")
        self.destination.addItem("LaGuardia Airport, New York")
        self.destination.addItem("Orlando International Airport, Orlando")
        self.destination.addItem("Miami International Airport, Miami")
        self.destination.addItem("Minneapolis-Saint Paul International Airport, Minneapolis")
        self.destination.addItem("Chicago O'Hare International Airport, Chicago")
        self.destination.addItem("Philadelphia International Airport, Philadelphia")
        self.destination.addItem("Phoenix Sky Harbor International Airport, Phoenix")
        self.destination.addItem("Seattle-Tacoma International Airport, Seattle")
        self.destination.addItem("San Francisco International Airport, San Francisco")

        self.daylabel=QLabel("Day",self)
        self.daylabel.move(75,320)
        self.daylabel.resize(100,30)
        self.daylabel.setFont(font)
        self.daylabel.setStyleSheet("color:white;")

        self.dayOfWeek=QComboBox(self)
        self.dayOfWeek.move(75,350)
        self.dayOfWeek.resize(175,30)
        self.dayOfWeek.setFont(font)
        
        self.dayOfWeek.addItem("Sunday")
        self.dayOfWeek.addItem("Monday")
        self.dayOfWeek.addItem("Tuesday")
        self.dayOfWeek.addItem("Wednesday")
        self.dayOfWeek.addItem("Thursday")
        self.dayOfWeek.addItem("Friday")
        self.dayOfWeek.addItem("Saturday")
        
        self.displaylabel=QLabel("",self)
        self.displaylabel.move(600,450)
        self.displaylabel.resize(200,30)
        self.displaylabel.setFont(font)
        self.displaylabel.setStyleSheet("color:white;")

        self.amountlabel=QLabel("",self)
        self.amountlabel.move(800,450)
        self.amountlabel.resize(200,30)
        self.amountlabel.setFont(font)
        self.amountlabel.setStyleSheet("color:white;")

        self.submitButton=QPushButton("View",self)
        self.submitButton.move(75,450)
        self.submitButton.resize(175,30)
        self.submitButton.setFont(font)
        self.submitButton.clicked.connect(self.Finder)

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)

    def Finder(self):
        
        l1=[]

        src=self.source.currentText().split(",")
        srcq=db.airports.find({'AIRPORT': src[0]})
        source=srcq[0]['IATA_CODE']

        dest=self.destination.currentText().split(",")
        destq=db.airports.find({'AIRPORT': dest[0]})
        destination=destq[0]['IATA_CODE']

        dayOfWeek=self.dayOfWeek.currentIndex()+1
        
        self.mainarea.clear()
        self.cursor=QTextCursor(self.mainarea.document())

        flq=db.flights.find({'ORIGIN_AIRPORT': source,'DESTINATION_AIRPORT': destination, 'DAY_OF_WEEK': dayOfWeek})
        
        self.displaylabel.setText("Total Number of Flights : ")
        self.amountlabel.setText(str(flq.count()))
        
        self.cursor.insertText("\nFlight No.\tAirline\tSch Dept.\tSch Arr.")

        for record in flq:
            self.cursor.insertText("\n{0}\t{1}\t{2}\t{3}".format(record['FLIGHT_NUMBER'],record['AIRLINE'],record['SCHEDULED_DEPARTURE'],record['SCHEDULED_ARRIVAL']))

            if record['AIRLINE'] not in l1:
                l1.append(record['AIRLINE'])

        self.cursor.insertText("\n\n\nAIRLINE CODES\n\n")

        slq=db.airlines.find({'IATA_CODE': {'$in' : l1}})

        for record in slq:
            self.cursor.insertText('{0}\t{1}\n'.format(record['IATA_CODE'],record['AIRLINE']))


class R4(QWidget):
    def __init__(self,parent=None):
        super(R4,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("Airline Statistics",self)
        self.mainlabel.move(75,80)
        self.mainlabel.resize(250,40)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.mainarea=QPlainTextEdit(self)
        self.mainarea.move(325,80)
        self.mainarea.resize(600,400)
        self.mainarea.setFont(font)

        self.airlinelabel=QLabel("Airline",self)
        self.airlinelabel.move(75,220)
        self.airlinelabel.resize(100,30)
        self.airlinelabel.setFont(font)
        self.airlinelabel.setStyleSheet("color:white;")

        self.airline=QComboBox(self)
        self.airline.move(75,250)
        self.airline.resize(200,30)
        self.airline.setFont(font) 

        self.airline.addItem("United Air Lines Inc.")
        self.airline.addItem("American Airlines Inc.")
        self.airline.addItem("US Airways Inc.")
        self.airline.addItem("Frontier Airlines Inc.")
        self.airline.addItem("JetBlue Airways")
        self.airline.addItem("Skywest Airlines Inc.")
        self.airline.addItem("Alaska Airlines Inc.")
        self.airline.addItem("Spirit Air Lines")
        self.airline.addItem("Southwest Airlines Co.")
        self.airline.addItem("Delta Air Lines Inc.")
        self.airline.addItem("Atlantic Southeast Airlines")
        self.airline.addItem("Hawaiian Airlines Inc.")
        self.airline.addItem("American Eagle Airlines Inc.")
        self.airline.addItem("Virgin America")
              
        self.submitButton=QPushButton("Search",self)
        self.submitButton.move(75,320)
        self.submitButton.resize(200,30)
        self.submitButton.setFont(font)
        self.submitButton.clicked.connect(self.Finder)

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)

    def Finder(self):
        
        airlq=db.airlines.find({'AIRLINE': self.airline.currentText()})
        airline=airlq[0]['IATA_CODE']

        self.mainarea.clear()
        self.cursor=QTextCursor(self.mainarea.document())

        flq = list(db.flights.aggregate([{"$group" : {'_id': "$AIRLINE", 'total': { "$avg": "$ARRIVAL_DELAY" },'MIN': {'$max': "$ARRIVAL_DELAY"},
            'MAX': {'$min': "$ARRIVAL_DELAY"},'DIV': { "$sum": "$DIVERTED" },'CAN': { "$sum": "$CANCELLED" }}},{'$project' : {'_id': '$_id' ,
               'roundedAvg' : { '$round': '$total' }, 'minDelay' : '$MIN','maxDelay' : '$MAX', 'diverted' : '$DIV','cancelled' : '$CAN'
           }}]))

        for i in flq:
            
            if(i['_id']==airline):

                if(i['roundedAvg']<0):
                    self.cursor.insertText('\n{0} minutes late on average\n\nMinimum Delay: {1}\nMaximum Delay: {2}\n\nCancelled : {3} in a week\nDiverted : {4} in a week'.format(i['roundedAvg'],i['maxDelay'],i['minDelay'],i['cancelled'],i['diverted']))

                elif(i['roundedAvg']==0):
                    self.cursor.insertText('\nOn Time on average\n\nMinimum Delay: {0}\nMaximum Delay: {1}\n\nCancelled : {2} in a week\nDiverted : {3} in a week'.format(i['maxDelay'],i['minDelay'],i['cancelled'],i['diverted']))

                else:
                    self.cursor.insertText('\n{0} minutes late on average\n\nMinimum Delay: {1}\nMaximum Delay: {2}\n\nCancelled : {3} in a week\nDiverted : {4} in a week'.format(i['roundedAvg'],i['maxDelay'],i['minDelay'],i['cancelled'],i['diverted']))

class R5(QWidget):
    def __init__(self,parent=None):
        super(R5,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("Database\nSchema",self)
        self.mainlabel.move(75,80)
        self.mainlabel.resize(250,80)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.mainarea=QPlainTextEdit(self)
        self.mainarea.move(325,80)
        self.mainarea.resize(600,400)
        self.mainarea.setFont(font)

        self.submitButton=QPushButton("View",self)
        self.submitButton.move(75,320)
        self.submitButton.resize(175,30)
        self.submitButton.setFont(font)
        self.submitButton.clicked.connect(self.Finder)

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)
    
    def Finder(self):
      
        self.mainarea.clear()
        self.cursor=QTextCursor(self.mainarea.document())

        flq= dict(flights.find_one())

        for key,value in flq.items():
            self.cursor.insertText(key+"\n")

class D1(QWidget):
    def __init__(self,parent=None):
        super(D1,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("Delete Flights\nby Airline on\nSpecific date",self)
        self.mainlabel.move(75,80)
        self.mainlabel.resize(250,100)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.mainarea=QPlainTextEdit(self)
        self.mainarea.move(350,80)
        self.mainarea.resize(575,400)
        self.mainarea.setFont(font)

        self.datelabel=QLabel("Date",self)
        self.datelabel.move(75,200)
        self.datelabel.resize(100,30)
        self.datelabel.setFont(font)
        self.datelabel.setStyleSheet("color:white;")

        self.date=QDateEdit(self)
        self.date.move(75,230)
        self.date.resize(200,30)
        self.date.setFont(font)
        self.date.setDate(QDate(2015,1,1))

        self.airlinelabel=QLabel("Airline",self)
        self.airlinelabel.move(75,290)
        self.airlinelabel.resize(100,30)
        self.airlinelabel.setFont(font)
        self.airlinelabel.setStyleSheet("color:white;")

        self.airline=QComboBox(self)
        self.airline.move(75,320)
        self.airline.resize(200,30)
        self.airline.addItem("United Air Lines Inc.")
        self.airline.addItem("American Airlines Inc.")
        self.airline.addItem("US Airways Inc.")
        self.airline.addItem("Frontier Airlines Inc.")
        self.airline.addItem("JetBlue Airways")
        self.airline.addItem("Skywest Airlines Inc.")
        self.airline.addItem("Alaska Airlines Inc.")
        self.airline.addItem("Spirit Air Lines")
        self.airline.addItem("Southwest Airlines Co.")
        self.airline.addItem("Delta Air Lines Inc.")
        self.airline.addItem("Atlantic Southeast Airlines")
        self.airline.addItem("Hawaiian Airlines Inc.")
        self.airline.addItem("American Eagle Airlines Inc.")
        self.airline.addItem("Virgin America")
        self.airline.setFont(font)
        self.airline.currentIndexChanged.connect(self.Adder)    

        self.submitButton=QPushButton("Search",self)
        self.submitButton.move(75,390)
        self.submitButton.resize(200,30)
        self.submitButton.setFont(font)
        self.submitButton.clicked.connect(self.Finder)

        self.deleteButton=QPushButton("Delete",self)
        self.deleteButton.move(75,450)
        self.deleteButton.resize(200,30)
        self.deleteButton.setFont(font)
        self.deleteButton.clicked.connect(self.Deleter)

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)
    global s,l1
    s=[]
    l1=[]

    def Adder(self,i):
        
        airx=self.airline.currentText()
        if airx not in l1:
            l1.append(airx)
        self.mainarea.clear()
        self.cursor=QTextCursor(self.mainarea.document())
        self.cursor.insertText("Selected Airlines")
        for rec in l1:
            self.cursor.insertText("\n{0}".format(rec))

        airlq=db.airlines.find({'AIRLINE': airx})
        airline=airlq[0]['IATA_CODE']
        if airline not in s:
            s.append(airline)
        print(s)
    
    def Finder(self):

        airlq=db.airlines.find({'AIRLINE': self.airline.currentText()})
        airline=airlq[0]['IATA_CODE']

        date=self.date.date().toPyDate()

        self.mainarea.clear()
        self.cursor=QTextCursor(self.mainarea.document())

        flq=flights.find({"AIRLINE" : {'$in' : s},'DAY' : date.day, 'MONTH' : date.month, 'YEAR' : date.year}).skip(7).limit(5)
        self.cursor.insertText("Flight No.\tSource\tDestination\t\tAirline\n")
        for record in flq:
            self.cursor.insertText("\n{0}\t{1}\t{2}\t\t{3}".format(record['FLIGHT_NUMBER'],record['ORIGIN_AIRPORT'],record['DESTINATION_AIRPORT'],record['AIRLINE']))

    def Deleter(self):
        
        date=self.date.date().toPyDate()
        dlq=flights.delete_many({"AIRLINE" : {'$in' : s},'DAY' : date.day, 'MONTH' : date.month, 'YEAR' : date.year})
        

class D2(QWidget):
    def __init__(self,parent=None):
        super(D2,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("Delete Flights\nby Delay",self)
        self.mainlabel.move(75,80)
        self.mainlabel.resize(250,80)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.mainarea=QPlainTextEdit(self)
        self.mainarea.move(325,80)
        self.mainarea.resize(600,400)
        self.mainarea.setFont(font)

        self.minlabel=QLabel("Min",self)
        self.minlabel.move(75,200)
        self.minlabel.resize(100,30)
        self.minlabel.setFont(font)
        self.minlabel.setStyleSheet("color:white;")

        self.min=QLineEdit(self)
        self.min.move(75,230)
        self.min.resize(175,30)
        self.min.setFont(font)

        self.maxlabel=QLabel("Max",self)
        self.maxlabel.move(75,290)
        self.maxlabel.resize(100,30)
        self.maxlabel.setFont(font)
        self.maxlabel.setStyleSheet("color:white;")

        self.max=QLineEdit(self)
        self.max.move(75,320)
        self.max.resize(175,30)
        self.max.setFont(font)

        self.submitButton=QPushButton("Search",self)
        self.submitButton.move(75,390)
        self.submitButton.resize(175,30)
        self.submitButton.setFont(font)
        self.submitButton.clicked.connect(self.Finder)

        self.deleteButton=QPushButton("Delete",self)
        self.deleteButton.move(75,450)
        self.deleteButton.resize(175,30)
        self.deleteButton.setFont(font)
        self.deleteButton.clicked.connect(self.Deleter)

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)
       
    def Finder(self):        

        max=int(self.max.text())
        min=int(self.min.text())

        self.mainarea.clear()
        self.cursor=QTextCursor(self.mainarea.document())

        flq=flights.find({'$or' : [{"ARRIVAL_DELAY" : {'$gt':max}},{"ARRIVAL_DELAY" : {'$lt':min}}]})
        self.cursor.insertText("Flight No.\tSource\tDestination\t\tDelay\n")
        for record in flq:
            self.cursor.insertText("\n{0}\t{1}\t{2}\t\t{3}".format(record['FLIGHT_NUMBER'],record['ORIGIN_AIRPORT'],record['DESTINATION_AIRPORT'],record['ARRIVAL_DELAY']))
                
    def Deleter(self):
        
        max=int(self.max.text())
        min=int(self.min.text())
        dlq=flights.delete_many({'$or' : [{"ARRIVAL_DELAY" : {'$gt':max}},{"ARRIVAL_DELAY" : {'$lt':min}}]})


class MLA(QWidget):
    def __init__(self,parent=None):
        super(MLA,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("Predict Delay",self)
        self.mainlabel.move(375,20)
        self.mainlabel.resize(250,40)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.mainarea=QTextEdit(self)
        self.mainarea.move(660,80)
        self.mainarea.resize(300,400)
        self.mainarea.setFont(font)

        self.airlinelabel=QLabel("Airline",self)
        self.airlinelabel.move(75,80)
        self.airlinelabel.resize(100,30)
        self.airlinelabel.setFont(font)
        self.airlinelabel.setStyleSheet("color:white;")

        self.airline=QComboBox(self)     # Creating dropdown
        self.airline.move(145,80)
        self.airline.resize(220,30)
        self.airline.setFont(font)

        self.airline.addItem("United Air Lines Inc.")
        self.airline.addItem("American Airlines Inc.")
        self.airline.addItem("US Airways Inc.")
        self.airline.addItem("Frontier Airlines Inc.")
        self.airline.addItem("JetBlue Airways")
        self.airline.addItem("Skywest Airlines Inc.")
        self.airline.addItem("Alaska Airlines Inc.")
        self.airline.addItem("Spirit Air Lines")
        self.airline.addItem("Southwest Airlines Co.")
        self.airline.addItem("Delta Air Lines Inc.")
        self.airline.addItem("Atlantic Southeast Airlines")
        self.airline.addItem("Hawaiian Airlines Inc.")
        self.airline.addItem("American Eagle Airlines Inc.")
        self.airline.addItem("Virgin America")
        
        self.flightlabel=QLabel("Fl Number",self)
        self.flightlabel.move(405,80)
        self.flightlabel.resize(100,30)
        self.flightlabel.setFont(font)
        self.flightlabel.setStyleSheet("color:white;")

        self.flightbox=QLineEdit(self)    # Creating input box
        self.flightbox.move(500,80)
        self.flightbox.resize(100,30)
        self.flightbox.setFont(font)

        self.sourcelabel=QLabel("Source",self)
        self.sourcelabel.move(75,145)
        self.sourcelabel.resize(100,30)
        self.sourcelabel.setFont(font)
        self.sourcelabel.setStyleSheet("color:white;")

        self.source=QComboBox(self)
        self.source.move(170,145)
        self.source.resize(430,30)
        self.source.setFont(font)

        self.source.addItem("Hartsfield-Jackson Atlanta International Airport, Atlanta")
        self.source.addItem("Gen. Edward Lawrence Logan International Airport, Boston")
        self.source.addItem("Charlotte Douglas International Airport, Charlotte")
        self.source.addItem("Denver International Airport, Denver")
        self.source.addItem("Dallas/Fort Worth International Airport, Dallas-Fort Worth")
        self.source.addItem("Detroit Metropolitan Airport, Detroit")
        self.source.addItem("Newark Liberty International Airport, Newark")
        self.source.addItem("George Bush Intercontinental Airport, Houston")
        self.source.addItem("John F. Kennedy International Airport, New York")
        self.source.addItem("McCarran International Airport, Las Vegas")
        self.source.addItem("Los Angeles International Airport, Los Angeles")
        self.source.addItem("LaGuardia Airport, New York")
        self.source.addItem("Orlando International Airport, Orlando")
        self.source.addItem("Miami International Airport, Miami")
        self.source.addItem("Minneapolis-Saint Paul International Airport, Minneapolis")
        self.source.addItem("Chicago O'Hare International Airport, Chicago")
        self.source.addItem("Philadelphia International Airport, Philadelphia")
        self.source.addItem("Phoenix Sky Harbor International Airport, Phoenix")
        self.source.addItem("Seattle-Tacoma International Airport, Seattle")
        self.source.addItem("San Francisco International Airport, San Francisco")
        
        self.destinationlabel=QLabel("Destination",self)
        self.destinationlabel.move(75,210)
        self.destinationlabel.resize(100,30)
        self.destinationlabel.setFont(font)
        self.destinationlabel.setStyleSheet("color:white;")

        self.destination=QComboBox(self)
        self.destination.move(170,210)
        self.destination.resize(430,30)
        self.destination.setFont(font)

        self.destination.addItem("Hartsfield-Jackson Atlanta International Airport, Atlanta")
        self.destination.addItem("Gen. Edward Lawrence Logan International Airport, Boston")
        self.destination.addItem("Charlotte Douglas International Airport, Charlotte")
        self.destination.addItem("Denver International Airport, Denver")
        self.destination.addItem("Dallas/Fort Worth International Airport, Dallas-Fort Worth")
        self.destination.addItem("Detroit Metropolitan Airport, Detroit")
        self.destination.addItem("Newark Liberty International Airport, Newark")
        self.destination.addItem("George Bush Intercontinental Airport, Houston")
        self.destination.addItem("John F. Kennedy International Airport, New York")
        self.destination.addItem("McCarran International Airport, Las Vegas")
        self.destination.addItem("Los Angeles International Airport, Los Angeles")
        self.destination.addItem("LaGuardia Airport, New York")
        self.destination.addItem("Orlando International Airport, Orlando")
        self.destination.addItem("Miami International Airport, Miami")
        self.destination.addItem("Minneapolis-Saint Paul International Airport, Minneapolis")
        self.destination.addItem("Chicago O'Hare International Airport, Chicago")
        self.destination.addItem("Philadelphia International Airport, Philadelphia")
        self.destination.addItem("Phoenix Sky Harbor International Airport, Phoenix")
        self.destination.addItem("Seattle-Tacoma International Airport, Seattle")
        self.destination.addItem("San Francisco International Airport, San Francisco")

        self.distancelabel=QLabel("Distance",self)
        self.distancelabel.move(75,405)
        self.distancelabel.resize(200,30)
        self.distancelabel.setFont(font)
        self.distancelabel.setStyleSheet("color:white;")
        
        self.distance=QSpinBox(self)    # Creating an input type for numbers
        self.distance.move(245,405)
        self.distance.resize(120,30)
        self.distance.setRange(0,10000)
        self.distance.setFont(font)

        self.schDeptlabel=QLabel("Scheduled Departure",self)
        self.schDeptlabel.move(75,275)
        self.schDeptlabel.setFont(font)
        self.schDeptlabel.setStyleSheet("color:white;")

        self.schDept=QDateTimeEdit(self)    # Creating a date and time input box
        self.schDept.move(245,275)
        self.schDept.resize(200,30)
        self.schDept.setFont(font)
        self.schDept.setDate(QDate(2015,1,1))   # Set default date in dateEdit box

        self.schArrlabel=QLabel("Schedued Arrival",self)
        self.schArrlabel.move(75,340)
        self.schArrlabel.setFont(font)
        self.schArrlabel.setStyleSheet("color:white;")

        self.schArr=QDateTimeEdit(self)
        self.schArr.move(245,340)
        self.schArr.resize(200,30)
        self.schArr.setFont(font)
        self.schArr.setDate(QDate(2015,1,1))

        self.predictButton=QPushButton("View Prediction",self)
        self.predictButton.move(75,465)
        self.predictButton.resize(200,30)
        self.predictButton.setFont(font)
        self.predictButton.clicked.connect(self.main)  

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)

    def timeFormat(self,time):   # Time format converter
        return int("%02d"%time.hour+"%02d"%time.minute)
    
    def timeDiff(self,dt1,dt2):   #Date time difference 
        diff=dt2-dt1
        return diff

    def encoded(self,list,airl):
        return list.index(airl)

    def Predictor(self,df):

        features = ['DAY',
        'DAY_OF_WEEK',
        'FLIGHT_NUMBER',
        'AIRLINE',
        'ORIGIN_AIRPORT',
        'DESTINATION_AIRPORT',
        'SCHEDULED_DEPARTURE',
        'DEPARTURE_DELAY',
        'SCHEDULED_TIME',
        'AIR_TIME',
        'ARRIVAL_TIME',
        'ARRIVAL_DELAY',
        'DISTANCE',
        'TARGET_NAME']

        df.dropna(how='any',subset=features, inplace=True)
        df.fillna(0, inplace=True)
        
        # carrier list, one hot encoding carrier
        airline_list = ["AA", "AS", "B6", "DL", "EV", "F9", "HA", "MQ", "NK", "OO", "UA", "VX", "WN","US"]
        #df['AIRLINE'].fillna(random.choice(airline_list), inplace=True)
        le = preprocessing.LabelEncoder()
        le.fit(airline_list)
        x_carrier = le.transform(df['AIRLINE'])

        delay_list=['ND','D']
        df['TARGET_NAME'].fillna(random.choice(delay_list),inplace=True)
        le1=preprocessing.LabelEncoder()
        le1.fit(delay_list)
        Y_delay=le1.transform(df['TARGET_NAME'])
        
        # prepare for X
        X = np.column_stack((x_carrier,df["MONTH"],df["DAY_OF_WEEK"],df['SCHEDULED_DEPARTURE'],df['SCHEDULED_TIME'],df['SCHEDULED_ARRIVAL'],df["FLIGHT_NUMBER"],df["DISTANCE"]))

        date=self.schDept.date().toPyDate()   # Get date of flight from the dateTimeEdit of schDept
        flight=self.flightbox.text()   # Get Flight Number
        if flight=='':   # In case left empty
            flight=0

        schDept=self.timeFormat(self.schDept.time().toPyTime())
        schArr=self.timeFormat(self.schArr.time().toPyTime())
        scheduled=int(self.timeDiff(self.schDept.dateTime().toPyDateTime(),self.schArr.dateTime().toPyDateTime()).total_seconds()/60)
        distance=self.distance.value()
        airlq=db.airlines.find({'AIRLINE': self.airline.currentText()})
        air=airlq[0]['IATA_CODE']
        airline=self.encoded(airline_list,air)

        y = list(df["TARGET_NAME"])
        
        self.mainarea.clear()
        self.cursor=QTextCursor(self.mainarea.document())

        X_predicition=[[airline,date.month,date.weekday()+1,schDept,scheduled,schArr,flight,distance]]


        clf = GaussianNB()
        clf.fit(X,y)
        predictions_gasussianNB =clf.predict(X_predicition)
        self.cursor.insertText("GaussianNB\nPrediction : {0}".format(predictions_gasussianNB))
        
        clf = GaussianNB()
        predicted = cross_val_predict(clf, X, y, cv=10)
        self.cursor.insertText("\nAccuracy : {0}".format("%02f"%metrics.accuracy_score(y, predicted)))

        
        clf = DecisionTreeClassifier(criterion='entropy')
        clf.fit(X,y)
        predictions_tree =clf.predict(X_predicition)
        self.cursor.insertText("\n\nDecision Tree\nPrediction : {0}".format(predictions_tree))
        
        clf = DecisionTreeClassifier(criterion='entropy')
        predicted = cross_val_predict(clf, X, y, cv=10)
        self.cursor.insertText("\nAccuracy : {0}".format("%02f"%metrics.accuracy_score(y, predicted)))


        clf = RandomForestClassifier(criterion='entropy', n_estimators=50)
        clf.fit(X,y)
        predictions_forest =clf.predict(X_predicition)
        self.cursor.insertText("\n\nRandom Forest\nPrediction : {0}".format(predictions_forest))
        
        clf = RandomForestClassifier(criterion='entropy', n_estimators=50)
        predicted = cross_val_predict(clf, X, y, cv=10)
        self.cursor.insertText("\nAccuracy : {0}".format("%02f"%metrics.accuracy_score(y, predicted)))
      

        clf = KNeighborsClassifier(n_neighbors=10)
        clf.fit(X,y)
        predictions_boost =clf.predict(X_predicition)
        self.cursor.insertText("\n\nKNeighborsClassifier\nPrediction : {0}".format(predictions_boost))
        
        clf = KNeighborsClassifier(n_neighbors=10)
        predicted = cross_val_predict(clf,X, y, cv=10)
        self.cursor.insertText("\nAccuracy : {0}".format("%02f"%metrics.accuracy_score(y, predicted)))
        
    def main(self):
        filename = "datafiles\\flights.csv"
        df = pd.read_csv(filename)
        #df.drop(df.columns[(10)], axis= 1, inplace= True)
        self.Predictor(df)

class MRO(QWidget):
    def __init__(self,parent=None):
        super(MRO,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("Map Reduce Operations",self)
        self.mainlabel.move(75,100)
        self.mainlabel.resize(300,40)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.m1Btn=QPushButton("Find Frequency of\nDiverted/Cancelled\nFlights by\nSource Airport",self)
        self.m1Btn.move(542,100)
        self.m1Btn.resize(150,150)
        self.m1Btn.setFont(font)

        self.m2Btn=QPushButton("Find Frequency of\nDiverted/Cancelled\nFlights by\nAirline",self)
        self.m2Btn.move(775,100)
        self.m2Btn.resize(150,150)
        self.m2Btn.setFont(font)

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)

class M1(QWidget):
    def __init__(self,parent=None):
        super(M1,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("Frequency of Diverted/Cancelled Flights",self)
        self.mainlabel.move(75,80)
        self.mainlabel.resize(470,40)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.mainarea=QTextEdit(self)
        self.mainarea.move(600,80)
        self.mainarea.resize(325,400)
        self.mainarea.setFont(font)

        self.sourcelabel=QLabel("Airport",self)
        self.sourcelabel.move(75,160)
        self.sourcelabel.resize(100,30)
        self.sourcelabel.setFont(font)
        self.sourcelabel.setStyleSheet("color:white;")

        self.source=QComboBox(self)
        self.source.move(75,190)
        self.source.resize(450,30)
        self.source.setFont(font)

        self.source.addItem("Hartsfield-Jackson Atlanta International Airport, Atlanta")
        self.source.addItem("Gen. Edward Lawrence Logan International Airport, Boston")
        self.source.addItem("Charlotte Douglas International Airport, Charlotte")
        self.source.addItem("Denver International Airport, Denver")
        self.source.addItem("Dallas/Fort Worth International Airport, Dallas-Fort Worth")
        self.source.addItem("Detroit Metropolitan Airport, Detroit")
        self.source.addItem("Newark Liberty International Airport, Newark")
        self.source.addItem("George Bush Intercontinental Airport, Houston")
        self.source.addItem("John F. Kennedy International Airport, New York")
        self.source.addItem("McCarran International Airport, Las Vegas")
        self.source.addItem("Los Angeles International Airport, Los Angeles")
        self.source.addItem("LaGuardia Airport, New York")
        self.source.addItem("Orlando International Airport, Orlando")
        self.source.addItem("Miami International Airport, Miami")
        self.source.addItem("Minneapolis-Saint Paul International Airport, Minneapolis")
        self.source.addItem("Chicago O'Hare International Airport, Chicago")
        self.source.addItem("Philadelphia International Airport, Philadelphia")
        self.source.addItem("Phoenix Sky Harbor International Airport, Phoenix")
        self.source.addItem("Seattle-Tacoma International Airport, Seattle")
        self.source.addItem("San Francisco International Airport, San Francisco")

        self.divertedlabel=QLabel("Diverted",self)
        self.divertedlabel.move(75,280)
        self.divertedlabel.resize(200,30)
        self.divertedlabel.setFont(font)
        self.divertedlabel.setStyleSheet("color:white;")

        self.diverted=QCheckBox(self)    # Creating a input type of radio button
        self.diverted.move(175,280)
        self.diverted.resize(15,30)
        self.diverted.setFont(font)
        
        self.cancelledlabel=QLabel("Cancelled",self)
        self.cancelledlabel.move(75,320)
        self.cancelledlabel.resize(200,30)
        self.cancelledlabel.setFont(font)
        self.cancelledlabel.setStyleSheet("color:white;")

        self.cancelled=QCheckBox(self)
        self.cancelled.move(175,320)
        self.cancelled.resize(15,30)
        self.cancelled.setFont(font)

        self.submitButton=QPushButton("View",self)
        self.submitButton.move(75,450)
        self.submitButton.resize(175,30)
        self.submitButton.setFont(font)
        self.submitButton.clicked.connect(self.Finder)

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)

    def Finder(self):
        
        src=self.source.currentText()
        splitted=src.split(",")
        srcq=db.airports.find({'AIRPORT': splitted[0]})
        source=srcq[0]['IATA_CODE']

        cancelled=int(self.cancelled.isChecked())   # 0--> if unchecked and 1 otherwise
        diverted=int(self.diverted.isChecked())

        self.mainarea.clear()
        self.cursor=QTextCursor(self.mainarea.document())
        
        if diverted == 1 :
            map1 = Code("function(){"
                "emit( this.DESTINATION_AIRPORT, this.DIVERTED );"
                "};"
                )
            reduce1 = Code("function( key, valArr ) {"
                  "return Array.sum( valArr );"
                "}"
                )
            result = db.flights.map_reduce( map1, reduce1,"DivertedFreq1");
            query = result.find().sort("value",-1)
            for i in query:
                if (i['_id']==source):
                    self.cursor.insertText("\nFrequency of Diverted Flights\n\nfrom : {0}\n\nis : {1}\n\n".format(src,i['value']))

        if cancelled == 1 :
            map2 = Code("function(){"
                 "emit( this.ORIGIN_AIRPORT, this.CANCELLED);"
                "};"
                )
            reduce2 = Code("function( key, valArr ) {"
                  "return Array.sum( valArr );"
                "}"
                )
            result = db.flights.map_reduce( map2, reduce2,"CancelledFreq1");
            query = result.find().sort("value",-1)
            for i in query:
                if (i['_id']==source):
                    self.cursor.insertText("\nFrequency of Cancelled Flights\n\nfrom : {0}\n\nis : {1}\n\n".format(src,i['value']))
  
class M2(QWidget):
    def __init__(self,parent=None):
        super(M2,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("Frequency of Diverted/Cancelled Flights",self)
        self.mainlabel.move(75,80)
        self.mainlabel.resize(470,40)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.mainarea=QTextEdit(self)
        self.mainarea.move(600,80)
        self.mainarea.resize(325,400)
        self.mainarea.setFont(font)

        self.airlinelabel=QLabel("Airline",self)
        self.airlinelabel.move(75,160)
        self.airlinelabel.resize(100,30)
        self.airlinelabel.setFont(font)
        self.airlinelabel.setStyleSheet("color:white;")

        self.airline=QComboBox(self)
        self.airline.move(75,190)
        self.airline.resize(200,30)
        self.airline.setFont(font) 

        self.airline.addItem("United Air Lines Inc.")
        self.airline.addItem("American Airlines Inc.")
        self.airline.addItem("US Airways Inc.")
        self.airline.addItem("Frontier Airlines Inc.")
        self.airline.addItem("JetBlue Airways")
        self.airline.addItem("Skywest Airlines Inc.")
        self.airline.addItem("Alaska Airlines Inc.")
        self.airline.addItem("Spirit Air Lines")
        self.airline.addItem("Southwest Airlines Co.")
        self.airline.addItem("Delta Air Lines Inc.")
        self.airline.addItem("Atlantic Southeast Airlines")
        self.airline.addItem("Hawaiian Airlines Inc.")
        self.airline.addItem("American Eagle Airlines Inc.")
        self.airline.addItem("Virgin America")
              
        self.divertedlabel=QLabel("Diverted",self)
        self.divertedlabel.move(75,280)
        self.divertedlabel.resize(200,30)
        self.divertedlabel.setFont(font)
        self.divertedlabel.setStyleSheet("color:white;")

        self.diverted=QCheckBox(self)    # Creating a input type of radio button
        self.diverted.move(175,280)
        self.diverted.resize(15,30)
        self.diverted.setFont(font)
        
        self.cancelledlabel=QLabel("Cancelled",self)
        self.cancelledlabel.move(75,320)
        self.cancelledlabel.resize(200,30)
        self.cancelledlabel.setFont(font)
        self.cancelledlabel.setStyleSheet("color:white;")

        self.cancelled=QCheckBox(self)
        self.cancelled.move(175,320)
        self.cancelled.resize(15,30)
        self.cancelled.setFont(font)

        self.submitButton=QPushButton("View",self)
        self.submitButton.move(75,450)
        self.submitButton.resize(175,30)
        self.submitButton.setFont(font)
        self.submitButton.clicked.connect(self.Finder)

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)

    def Finder(self):
        
        airl=self.airline.currentText()
        airlq=db.airlines.find({'AIRLINE': airl})
        airline=airlq[0]['IATA_CODE']

        cancelled=int(self.cancelled.isChecked())   # 0--> if unchecked and 1 otherwise
        diverted=int(self.diverted.isChecked())

        self.mainarea.clear()
        self.cursor=QTextCursor(self.mainarea.document())
        
        if diverted == 1 :
            map3ii = Code("function(){"
                         "emit( this.AIRLINE, this.DIVERTED );"
                        "};"
                        )
            reduce3 = Code("function( key, valArr ) {"
                          "return Array.sum( valArr );"
                        "}"
                        )
            result = db.flights.map_reduce( map3ii, reduce3,"DivertedFreq");
            query = result.find().sort("value",-1)
            for i in query:
                if (i['_id']==airline):
                    self.cursor.insertText("\nFrequency of Diverted Flights\n\nby : {0}\n\nis : {1}\n\n".format(airl,i['value']))

        if cancelled == 1 :
            map3i = Code("function(){"
                         "emit( this.AIRLINE, this.CANCELLED);"
                        "};"
                        )
            reduce3 = Code("function( key, valArr ) {"
                          "return Array.sum( valArr );"
                        "}"
                        )
            result = db.flights.map_reduce( map3i, reduce3,"CancelledFreq");
            query = result.find().sort("value",-1)
            for i in query:
                if (i['_id']==airline):
                    self.cursor.insertText("\nFrequency of Cancelled Flights\n\nby : {0}\n\nis : {1}\n\n".format(airl,i['value']))

class VIS(QWidget):
    def __init__(self,parent=None):
        super(VIS,self).__init__(parent)
        self.InitUi()

    def InitUi(self):

        self.mainlabel=QLabel("Visualization Reports",self)
        self.mainlabel.move(350,20)
        self.mainlabel.resize(300,40)
        self.mainlabel.setFont(fontmain)
        self.mainlabel.setStyleSheet("color:white;")

        self.vis1Btn=QPushButton("Pie Chart",self)
        self.vis1Btn.move(75,100)
        self.vis1Btn.resize(150,150)
        self.vis1Btn.setFont(font)

        self.vis2Btn=QPushButton("Line Chart",self)
        self.vis2Btn.move(75,325)
        self.vis2Btn.resize(150,150)
        self.vis2Btn.setFont(font)

        self.vis3Btn=QPushButton("USA Map",self)
        self.vis3Btn.move(250,100)
        self.vis3Btn.resize(150,150)
        self.vis3Btn.setFont(font)

        self.vis4Btn=QPushButton("Seaborn\nVisualization",self)
        self.vis4Btn.move(250,325)
        self.vis4Btn.resize(150,150)
        self.vis4Btn.setFont(font)
        self.vis4Btn.clicked.connect(self.DisplayMap)

        self.imagelabel=QLabel("",self)
        #self.imagelabel.move(542,100)
        #self.imagelabel.resize(400,550)      

        self.backButton=QPushButton("Back",self)
        self.backButton.move(900,530)
        self.backButton.resize(80,30)
        self.backButton.setFont(font)

    def DisplayMap(self):
        self.imagelabel.setPixmap(QPixmap('images\\heatmap.png'))
        self.imagelabel.setGeometry(430,85,560,450)
  
class MainWindow(QMainWindow):    # The main window --> anything here will we displayed over top of other windows
    def __init__(self, parent=None):    # Call constructor
        super(MainWindow, self).__init__(parent)
        self.setGeometry(100, 50, 1000, 600)    # Set geometryb of application frame ---> left-margin, top-margin, width, height
        self.setWindowIcon(QIcon("images\\icon.png"))    # Set icon to the window

        self.backimage=QLabel(self)    # Creating a display label
        self.backimage.setPixmap(QPixmap('images\\background.jpg'))    # Set background.jpg in the label using pixmap
        self.backimage.setGeometry(0,0,1000,600)    # Set geometry of background image 

        mainMenu=self.menuBar()    # Creating a Menu Bar
        
        homeMenu=mainMenu.addMenu("HOME")    #Adding Menu Items
        crudMenu=mainMenu.addMenu("CRUD")
        mlMenu=mainMenu.addMenu("ML")
        visMenu=mainMenu.addMenu("Visualization")

        # Creating sub-menu actions

        homeButton=QAction(QIcon("images\\home.png"),'Home',self)   # Arguments are icon, name and self 
        homeButton.setShortcut("Ctrl+H")    # To create shortcut for the action
        homeButton.triggered.connect(self.startHome)    # Creating signal -- if trigggered will call function startHome()
        
        exitButton=QAction(QIcon("images\\exit.png"),'Exit',self)
        exitButton.setShortcut("Ctrl+E")
        exitButton.triggered.connect(self.Close)

        insertButton=QAction(QIcon("images\\insert.png"),'Insert',self)
        insertButton.setShortcut("Ctrl+I")
        insertButton.triggered.connect(self.startInsert)

        readButton=QAction(QIcon("images\\read.png"),'Read',self)
        readButton.setShortcut("Ctrl+R")
        readButton.triggered.connect(self.startCRUD1)

        deleteButton=QAction(QIcon("images\\delete.png"),'Delete',self)
        deleteButton.setShortcut("Ctrl+D")
        #deleteButton.triggered.connect(self.startCRUD2)

        algo1Button=QAction(QIcon("images\\ml.png"),'Algorithm Analysis',self)
        algo1Button.setShortcut("Ctrl+A")
        algo1Button.triggered.connect(self.startMLA)

        vis1Button=QAction(QIcon("images\\pie.png"),'Distance Coverage',self)
        vis1Button.triggered.connect(self.openVis1)

        vis2Button=QAction(QIcon("images\\line.png"),'Delay Chart',self)
        vis2Button.triggered.connect(self.openVis2)

        vis3Button=QAction(QIcon("images\\map.png"),'Flight Frequency',self)
        vis3Button.triggered.connect(self.openVis3)  
        
        # Adding Actions to their Menu

        homeMenu.addAction(homeButton)
        homeMenu.addAction(exitButton)

        crudMenu.addAction(insertButton)
        crudMenu.addAction(readButton)
        crudMenu.addAction(deleteButton)

        mlMenu.addAction(algo1Button)

        visMenu.addAction(vis1Button)
        visMenu.addAction(vis2Button)
        visMenu.addAction(vis3Button)

        # Calling the home function
        self.startHome()

    # Functions to call different classes ---> Enabling their visibility
    def startHome(self):
        self.Window = Home(self)   # Create instance of the class Home of type QWidget
        self.setCentralWidget(self.Window)    # Setting central Widged=Window
        self.setWindowTitle("Flight Application")   # Setting Titles
        self.Window.crudButton.clicked.connect(self.startCRUD1)  # Binding button clicks to functions. Written here as they call functions outside their classes
        self.Window.mlButton.clicked.connect(self.startMLA)
        self.Window.mpButton.clicked.connect(self.startMRO)
        self.Window.visButton.clicked.connect(self.startVIS)
        self.show()   # Open the window
 
    def Close(self):   # Exit Function
        reply=QMessageBox.question(self,"Close Message","Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)    # Dialog Box
        if reply==QMessageBox.Yes:
            self.close()    # Closing the Window

    def startInsert(self):
        self.InsertWindow = Insert(self)
        self.setWindowTitle("Insert Window")
        self.setCentralWidget(self.InsertWindow)
        self.InsertWindow.backButton.clicked.connect(self.startCRUD1)      
        self.show()
    
    def startCRUD1(self):
        self.CRUD1Window = CRUD1(self)
        self.setWindowTitle("CRUD WINDOW")
        self.setCentralWidget(self.CRUD1Window)
        self.CRUD1Window.r1Btn.clicked.connect(self.startR1)
        self.CRUD1Window.r2Btn.clicked.connect(self.startR2)
        self.CRUD1Window.r3Btn.clicked.connect(self.startR3)
        self.CRUD1Window.r4Btn.clicked.connect(self.startR4)
        self.CRUD1Window.i1Btn.clicked.connect(self.startInsert)
        self.CRUD1Window.d1Btn.clicked.connect(self.startD1)
        self.CRUD1Window.d2Btn.clicked.connect(self.startD2)
        self.CRUD1Window.backButton.clicked.connect(self.startHome)
        self.show()

    def startMLA(self):
        self.MLAWindow = MLA(self)
        self.setWindowTitle("ML ALGORITHMS")
        self.setCentralWidget(self.MLAWindow)
        self.MLAWindow.backButton.clicked.connect(self.startHome)
        self.show()
    
    def startVIS(self):
        self.VISWindow = VIS(self)
        self.setWindowTitle("VISUALIZATION REPORTS")
        self.setCentralWidget(self.VISWindow)
        self.VISWindow.backButton.clicked.connect(self.startHome)
        self.VISWindow.vis1Btn.clicked.connect(self.openVis1)
        self.VISWindow.vis2Btn.clicked.connect(self.openVis2)
        self.VISWindow.vis3Btn.clicked.connect(self.openVis3)
        self.show()

    def startMRO(self):
        self.MROWindow = MRO(self)
        self.setWindowTitle("ML ALGORITHMS")
        self.setCentralWidget(self.MROWindow)
        self.MROWindow.backButton.clicked.connect(self.startHome)
        self.MROWindow.m1Btn.clicked.connect(self.startM1)
        self.MROWindow.m2Btn.clicked.connect(self.startM2)
        self.show()

    def startR1(self):
        self.R1Window = R1(self)
        self.setWindowTitle("Read")
        self.setCentralWidget(self.R1Window)
        self.R1Window.backButton.clicked.connect(self.startCRUD1)
        self.show()

    def startR2(self):
        self.R2Window = R2(self)
        self.setWindowTitle("Read")
        self.setCentralWidget(self.R2Window)
        self.R2Window.backButton.clicked.connect(self.startCRUD1)
        self.show()

    def startR3(self):
        self.R3Window = R3(self)
        self.setWindowTitle("Read")
        self.setCentralWidget(self.R3Window)
        self.R3Window.backButton.clicked.connect(self.startCRUD1)
        self.show()

    def startR4(self):
        self.R4Window = R4(self)
        self.setWindowTitle("Read")
        self.setCentralWidget(self.R4Window)
        self.R4Window.backButton.clicked.connect(self.startCRUD1)
        self.show()
    
    def startR5(self):
        self.R5Window = R5(self)
        self.setWindowTitle("Read")
        self.setCentralWidget(self.R5Window)
        self.R5Window.backButton.clicked.connect(self.startCRUD1)
        self.show()
    
    def startD1(self):
        self.D1Window = D1(self)
        self.setWindowTitle("Delete")
        self.setCentralWidget(self.D1Window)
        self.D1Window.backButton.clicked.connect(self.startCRUD1)
        self.show()

    def startD2(self):
        self.D2Window = D2(self)
        self.setWindowTitle("Delete")
        self.setCentralWidget(self.D2Window)
        self.D2Window.backButton.clicked.connect(self.startCRUD1)
        self.show()

    def startM1(self):
        self.M1Window = M1(self)
        self.setWindowTitle("Map Reduce")
        self.setCentralWidget(self.M1Window)
        self.M1Window.backButton.clicked.connect(self.startMRO)
        self.show()

    def startM2(self):
        self.M2Window = M2(self)
        self.setWindowTitle("Map Reduce")
        self.setCentralWidget(self.M2Window)
        self.M2Window.backButton.clicked.connect(self.startMRO)
        self.show()

    def openVis1(self):
        QDesktopServices.openUrl(QUrl("http://localhost/bda/piechart.html"))   # Opens the url in a web browser

    def openVis2(self):
        QDesktopServices.openUrl(QUrl("http://localhost/bda/departure.html"))  
    
    def openVis3(self):
        QDesktopServices.openUrl(QUrl("http://localhost/bda/usmap.html")) 

if __name__ == '__main__':   # The main function
    app = QApplication(sys.argv)   # Creating the application
    w = MainWindow()   # Creating window Instance
    sys.exit(app.exec_())   # Execute application