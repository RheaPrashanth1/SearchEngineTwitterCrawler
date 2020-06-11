#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
from lxml.html import parse
import urllib.request as urllib2
import os
from pathlib import Path




# Enter Twitter API Keys
access_token = "3028914487-zriqd4Qo4DUjj1IJZbAPC6McsaALwYiSMICvfms"
access_token_secret = "u929aKlFsSRjT2eTAOhBWIj2hd4FYVJjeU5nTqkXwH2GV"
consumer_key = "r9Zv2p5DWekyQnC1aXHD8k5ks"
consumer_secret = "QITRb64e44ChymHmYFKRWSAjS43TbJmCA8fwa2G6AtEnnvNm7t"
filenum = 0

title = None
newfile = "tweet" + str(filenum) + ".txt"
OF = open(newfile, 'a')
#title = 5
#outF = open("tweet.txt", "w")
#outF = open("tweet.txt", "w")

# Listener class inherits from StreamListener
class Listener(StreamListener):
    def on_connect(self):
        print("connection is made")  


    def on_data(self,data):
        global tweetCount 
        global OF
        global filenum 
        global title
        global newfile
       # global title
      
        Dict = json.loads(data)  #JSON object to python DICT
        tweetURLS = Dict["entities"]["urls"]
       # Dict.update({"before" : 23}) #append to DICT
       # finalTweet = json.dumps(Dict) #convert DICT to JSON
        
       # OF.write(finalTweet + "\n") #put JSON objects one at a time on newline
       # print(finalTweet)

      #  print("newfile size: " , Path(newfile).stat().st_size)
        #if  Path(newfile).stat().st_size >= 3*1024:
        if OF.tell() >= 10 * 1024 * 1024:
          
            OF.close()
            filenum = filenum + 1
            newfile = "tweet" + str(filenum) + ".txt"
            OF = open(newfile, "a")
        
       # print("filenum: ", filenum)
        
        if filenum > 199:  #If 2GB of total data, stop streaming
            OF.close()
            print("StreamListener no longer streaming tweets - reached 2GB")
            return False
        
        if tweetURLS!= []:
            encodedUrl = Dict['entities']['urls'][0]['expanded_url']
            try:
                openedURL = urllib2.urlopen(encodedUrl)
                parsedPage = parse(openedURL)
                title = parsedPage.find(".//title").text
                
            except:
                print("There has been an error")
                return True
				
           # print(title)
        #title = parsedPage.find(".//title").text  
        if tweetURLS == []:
            title = None
            
            
        if title == None:
            Dict.update({"Title" : "None"}) #Python Dict with appended Title(none)
            appended = json.dumps(Dict) 
        
        if  title != None:
             ##encode title
            Dict.update({"Title" : title}) #Python Dict with appended Title
           # print(Dict["Title"])
            appended = json.dumps(Dict) #pythonDict to JSON
            
       
        OF.write(appended + "\n")
        print("newfile size: " , Path(newfile).stat().st_size)
        print(newfile)
        #Check if it can be read back
        app = json.loads(appended) #python dict
        #checkIfReadable = app["Title"]
        
        
        
        
        return True
        
    
    def on_error(self, tweetstatus):
        if tweetstatus == 420:
            print("Error occured, loser")
        if tweetstatus == 401:
            print("Authentication error")
            return False

    


if __name__ == '__main__':  
#Connect to twitter stream w/ authentication information
    
    L = Listener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, L)
    stream.filter(locations=[-125.156250,25.720735,-62.226563,49.496675],languages=["en"]) 
    #LA, Huntington Park, -> La Habra
    