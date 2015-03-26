#  Title: twitterHeat.py
#   Requirement: Google Earth
#                        streamer.py
#                        heatStream.txt (Provided by streamer.py)
#
#   Abstract: This program will take the text file created from streamer.py (Twitter Feed) and create a
#                Heat Map overlay will display it on Google Earth. The program will create points based on
#                the emotion value assigned from Twitter. The user will be asked to select the emotion
#                rating to display.
#  Author: Jeremy Gutierrez
#  ID: 4093
#  Contributer: Pierce Reinsch
#
#  Date: 03/25/2015
#

import sys # used for sys operations w/ files
import heatmap # Used for the Heatmap Overlay
import random # Used for demo of the Heatmap
import os # Used for opening the file
from decimal import Decimal # Used for the decimal conversion

def heatMap(pts, option): #This will create the heat Map overlay for Google Earth
    hm = heatmap.Heatmap()
    if option is 1: # If positive use color scheme pbj
        hm.heatmap(pts, dotsize = 10, scheme = 'omg', opacity = 250)
    elif option is 2: # if negative use color scheme classic
        hm.heatmap(pts, dotsize = 10, scheme = 'pbj', opacity = 250)
    elif option is 3: # if nuetral use omg color scheme
        hm.heatmap(pts, dotsize = 10, scheme = 'classic', opacity = 250)
    else: # all use the fire color scheme
        hm.heatmap(pts, dotsize = 10, scheme = 'fire', opacity = 250)
    hm.saveKML("C:/CST205/twitterHeat/heatData.kml") # This will save a .kml  & a png image that will be used w/ Google Earth.

def openMap(): # This will open Google Earth and display the map
    os.system('"C:/CST205/twitterHeat/heatData.kml"')

def readFile(ind, lat, log): # This will read the text file sent from streamer.py
    arr = []
    data = open ("heatStream.txt","r") #Open File
    for line in data.readlines(): # Read lines
        for i in line.split(): # Seperate into an array
            arr.append(str(i))
    j = len(arr) - 1
    k = j / 3 # This will determine the number of entries in the file
    while k%3 !=0: # Checks to make sure last line in streamer is complete w/ 3 entries
        j = j-1 # not complete. remove 1 entry
        k = j / 3 #change count and retest
    while (k != -1): # For x amount  entries in the file seperate elements
        log.append(arr[j]) # Append the longitude to longitude array
        j = j - 1
        lat.append(arr[j]) # Append the latitude to latitude array
        j = j - 1
        ind.append(arr[j]) # Append index value to index array
        j = j - 1
        k = k - 1 # counter

def positiveEmo(ind, lat, log, pts, option): # this will create the coordinates for postive emotions
        i = len(ind)  #number of incoming coordinates
        j = i - 1
        pt = []
        while (j != 0):
            val = str(Decimal(ind[j]) * 10) # change the value to a whole number  & ignore anything beyind the decimal
            if (val >= "4"): # for Positive emotion value add to list
                j = j - 1
                x = float(lat[j])
                y = float(log[j])
                pt = [x,y]
                pts.append(pt)
            else:
                j = j - 1

def negativeEmo(ind, lat, log, pts, option):
        i = len(ind)  #number of incoming coordinates
        j = i - 1
        pt = []
        while (j != 0):
            val = str(Decimal(ind[j]) * -10) # Flip to negative and positve, switch to whole, and ignore decimal
            if (val >= "4"):# for negative emotion value add to list
                j = j - 1
                x = float(lat[j])
                y = float(log[j])
                pt = [x,y]
                pts.append(pt)
            else:
                j = j - 1

def nuetralEmo(ind, lat, log, pts, option):
        i = len(ind)  #number of incoming coordinates
        j = i - 1
        pt = []
        while (j != 0):
            valNeg = str(Decimal(ind[j]) * -10) # Flip to negative and positve, switch to whole, and ignore decimal
            valPos = str(Decimal(ind[j]) * 10)  # change the value to a whole number  & ignore anything beyind the decimal
            if (valNeg <= "4" or valPos <= "4"):
                j = j - 1
                x = float(lat[j])
                y = float(log[j])
                pt = [x,y]
                pts.append(pt)
            else:
                j = j - 1

def allEmo(ind, lat, log, pts, option): # include all points
        i = len(ind)  #number of incoming coordinates
        j = i - 1
        pt = []
        while (j != 0):
            j = j - 1
            x = float(lat[j])
            y = float(log[j])
            pt = [x,y]
            pts.append(pt)

def main():
    ind = [] # List for research Index
    lat = [] # List for latitude
    log = [] #List for longitude
    pts = []
    readFile(ind, lat, log) # Will read the information collected from the Twitter file
    option = input('Please select an Emotion Value\n 1. Positive Emotion\n 2. Negative Emotion\n 3. Nuetral Emotion\n 4. All\nWhat would you like to see #  ')
    if (option == 1): # Will show the heatimage for positive emotions.
        positiveEmo(ind, lat, log, pts, option)
    elif (option == 2): # Will show the heatimage for negative emotions
        negativeEmo(ind, lat, log, pts, option)
    elif (option== 3): # Will show the heatimage for nuetral emotions
        nuetralEmo(ind, lat, log, pts, option)
    else: # Will show the heatimage for all
        allEmo(ind, lat, log, pts, option)
    heatMap(pts, option) # Used to call create Heat Map Overlay
    openMap() # Used to call open map command

main()


