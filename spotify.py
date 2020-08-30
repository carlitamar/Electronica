import os
import sys
import requests
import json
import spotipy
import webbrowser
import spotipy.util as util
from  json.decoder import JSONDecodeError
import requests
import time
import serial

arduino = serial.Serial("/dev/cu.usbmodemFA131", 9600)

#Get the username from terminal
username = input("Cuál es tu nombre/número de usuario: ")

#Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

#create spotify object
spotifyObject =  spotipy.Spotify(auth=token)

user = spotifyObject.current_user()
print(json.dumps(user, sort_keys=True, indent=4))

displayName = user['display_name']

while True:

    print()
    print(">>>Welcome to Spotipy " + displayName + "!<<<")
    print()
    print(">>>0 - Search for a song")
    print(">>>1 - Exit")
    print()
    choice = input("Your choice: ")

    #search for the artist
    if choice == "0":
        print()
        searchQuery = input("Select a song name: ") 
        print()

        #get search results
        searchResults = spotifyObject.search(searchQuery,  1, 0, "track")
        print(json.dumps(searchResults, sort_keys=True, indent=4))

        dance = spotifyObject.audio_features(searchResults['tracks']['items'][0]['id'])
        #print(json.dumps(dance, sort_keys=True, indent=4))
        danceability = dance[0]['danceability']
        print(">>>DANCEABILITY<<<")
        print()
        print(danceability)
        print()
        
        trackid = searchResults['tracks']['items'][0]['id']

        #for playback
        #context_uri = searchResults['tracks']['items'][0]['album']['artists'][0]['uri']
        uris = searchResults['tracks']['items'][0]['uri']
        #spotifyObject.start_playback(None,None,uris,None)
    
        beats = spotifyObject.audio_analysis(trackid)
        #print(json.dumps(beats, sort_keys=True, indent=4))

        sumtime = beats['beats'][0]['start']
        #print(sumtime)
    
        print(">>>BEATS<<<")
        print()

        if (danceability <= 0.4):
            for x in range(0, 1000):
                arduino.write('A'.encode()) #matriz2
                timestart = beats['beats'][x]['start']
                print("ON: " + str(timestart))
                print()
                time.sleep(beats['beats'][x]['duration']/2)
                arduino.write('B'.encode()) #matriz3
                print("OFF")
                print()
                time.sleep((beats['beats'][x]['duration'])/2)
        elif (danceability > 0.4 and danceability <= 0.666):
            for x in range(0, 1000):
                arduino.write('A'.encode()) #matriz2
                timestart = beats['beats'][x]['start']
                print("ON: " + str(timestart))
                print()
                time.sleep(beats['beats'][x]['duration']/2)
                arduino.write('C'.encode()) #matriz4
                print("OFF")
                print()
                time.sleep((beats['beats'][x]['duration'])/2)
        elif (danceability > 0.666):
            for x in range(0, 1000):
                arduino.write('D'.encode()) #matriz5
                timestart = beats['beats'][x]['start']
                print("ON: " + str(timestart))
                print()
                time.sleep(beats['beats'][x]['duration']/2)
                arduino.write('E'.encode()) #matriz6
                print("OFF")
                print()
                time.sleep((beats['beats'][x]['duration'])/2)
    if choice == "1":
        break


#print(json.dumps(VARIABLE, sort_keys=True, indent=4))
#Username/User ID: 12144681031
#export SPOTIPY_CLIENT_ID='030cf17c004b4c91b2c85f9c58c19089'
#export SPOTIPY_CLIENT_SECRET='6463dece33b54dc8b3aef20f6d308ab4'
#export SPOTIPY_REDIRECT_URI='http://google.com/'

#device = spotifyObject.devices()
#print(json.dumps(device, sort_keys=True, indent=4))





