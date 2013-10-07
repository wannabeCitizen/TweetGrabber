#Script for creating Twitter API requests and saving the responses as JSON blobs

import TwitterAPI    #importing TwitterAPI library for handling API requests
import ujson as json       #import ujson for handling json data
from config import access_tokens    #import access codes from a config file I have saved elsewhere
import os                           #import os module for making directories
import time                         #import time module for getting timestamps


def archive_endpoint(endpoint, name):    #function that takes in command for which twitter API request I'm going to make and a name for this request
    print "[%s] Running archive_endpoint for %s" % (time.time(), endpoint)  #print statement to let me know the script is running in my log
    api = TwitterAPI.TwitterAPI(**access_tokens)                #create TwitterAPI object for request
    
    params = {'count':200}                                      #creating dict object for my parameters to send in my request - includes a max count for response
    try:
        min_id = json.load(open("max_ID_%s" % name))            #grab the biggest ID from my last API request, and make this my min ID for my new request
        params.update(min_id)                                   #update my parameters with this number
    except:
        print "This is the first time this has been run"       #print letting me know there was no ID in the file
    
    print "Making request to twitter"                          #Let's me know the Twitter request is being made
    updated_timeline = api.request(endpoint, params)           #set object for Twitter response
    data_file = time.strftime("%Y/%m/%d/%H-" + name)            #Set up a datafile to dump the response in
    
    try:
        directory = os.path.dirname(data_file)                  #parse out the directory from the file name
        os.makedirs(directory)                                  #make the directory for my file, if it doesn't exist
    except:
        print "directory already exists"                        #Lets me know if it did already exist
    
    new_id = 0                                                  #Initiate my new_id variable for keeping track of id #'s as I parse the data
    
    print "Saving data"                                         #Let's me know the data saving phase has started
    with open(data_file, "a+") as fd:                           #With statement to open up my datafile for writing
        count = 0                                               #counter for keeping track of number of new tweets I upload
        for item in updated_timeline.get_iterator():            #for loop to iterate over all responses from Twitter
            new_json = json.dumps(item) + '\n'                  #dump the string response from twitter into a json object
            fd.write(new_json)                                  #Write that json to my file that is open
            new_id = max(new_id, item['id'])                    #Check to see if this is the largest ID i've seen
            count += 1                                          #increment my count 
        print "Saved %d items" % count                          #Print how many new items I saved

    if new_id:                                                  #checks to see if I got a new ID #
        print "Saving new_id = %d" % new_id                     #prints the new ID to me
        future_load_value = {"since_id" : new_id}               #sets the ID # into a dict that is set up like a parameter request to Twitter
        json.dump(future_load_value, open("max_ID_%s" % name, "w+"))    #dump that value into the file that stores my max ID

if __name__ == "__main__":                                          #Checks if I'm calling this file from terminal
    archive_endpoint("statuses/home_timeline", "timeline")          #Calls my function
    
