'''Streaming code By: Pearce Reinsch
    In collaboration with: Jeremy Gutierrez'''

# -*- coding: UTF-8 -*-
import tweepy
import json
import sys
import vaderSentiment.vaderSentiment as SA

consumer_key = 'ECb2LfdGGqLTsRB0BoZIwurVI'                              # Twitter API
consumer_secret = 'YCW7OmxQz3hGJuS0da6FIdibm8Wi6ylpNAqsU3asCMxnJC5pxh'  #  access keys
access_token = '2833184940-lM3SDLzHZ9pVAzuyEOIniJ3CIDBIFPamLc0fwIq'     #
access_token_secret = 'Qjd66cI2EK6DGdL8HZ7AAJYxwHZodSkIwfsAwsUM3lVYW'   #
targetTime = 0

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)               # setting up
auth.set_access_token(access_token, access_token_secret)                # Twitter server
api = tweepy.API(auth)                                                  # auth request

class MyStreamListener(tweepy.StreamListener):                          # creates Twitter streaming object
    def __init__(self, api = None):                                     # sets up initial construction of streaming object
        self.api = api                                                  # stores which API being used and connection auth details
        self.output = open("heatStream" +'.txt', 'w')                   # creates file to store parsed information

    def on_status(self, status):                                        # runs function whenever a status is streamed from server
        if 'coordinates' in status:                                     # if the status has a coordinate:
            status_dict = json.loads(status)                            #       convert the status json into a python dictionary
            tweet = status_dict['text']                                 #       temporarily store the text of the tweet
            if status_dict['coordinates'] != None:                      #       as long as there is a non-NULL coordinate:
                if 'coordinates' in status_dict['coordinates']:         #           and there is actually a coordinate:
                    try:                                                #             Attempt to:
                        SA.sentiment(tweet)                             #               rate the sentiment of the saved text
                        self.print_things(status_dict)                  #               and run the function save data to txt file
                    except:                                             #             If Attempt fails:
                        return                                          #               end function to get next status
        return                                                          # if there are no matches, end function to get next status

    def on_data(self, data):                                            # runs any time data is received through the stream
        self.on_status(data)                                            #   and passes the data to the status parsing function
        return True                                                     #

    def on_error(self, status):                                         # runs if there is an error received through the stream
        print status                                                    #  prints the error to the terminal
        return False                                                    #

    def on_timeout(self):                                               # runs if there is a timeout error through the stream
        print "Timeout"                                                 #  prints error message to the terminal
        return                                                          #

    def print_things(self, status_dict):                                # saves pertinent information from the status when called
        senti = str(SA.sentiment(status_dict['text'])['compound'])      # stores the sentiment analysis score
        coord1 = str(status_dict['coordinates']['coordinates'][0])      # stores the latitude from the tweet coordinate
        coord2 = str(status_dict['coordinates']['coordinates'][1])      # stores the longitude from the tweet coordinate
        try:                                                            #
            self.output.write(senti +' '+ coord1 +' '+ coord2 +'\n')    # attempts to write the above stored values to txt file
        except:                                                         #
            return                                                      #
        return                                                          #

def main():
    MSL = MyStreamListener(api)                                         # initiates a new streaming object
    stream = tweepy.streaming.Stream(auth, MSL)                         # begins stream auth with twitter server
                                                                        #
    print "Stream connected"                                            # is able to auth to server prints message to terminal
                                                                        #
    try:                                                                #
        stream.filter(locations = [-179.75,-85.3,179.75,84.8])          # filters incoming stream to those within coordinates
    except:                                                             #
        print "Stream Disconnected"                                     # if stream fails then print error to terminal
        stream.disconnect()                                             # and disconnect the stream

if __name__ == '__main__':                                              #
    main()                                                              # runs main function