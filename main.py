import os
import json

#to stop opening the file again and again - we can open it once here and make it global (optimize)
def file_open(playlist_name = "playlist1.json"):
    f = open("playlist1.json")
    global data
    data = json.load(f)
    f.close()
    return data


#user needs to input the file name with all their spotify data (default spotify data is given as "playlist1.json")
def data_parse(): 
    global playlist_names
    global playlist_dict
    playlist_names = []
    playlist_dict = {}
    
    try:
        for i in data["playlists"]:
            playlist_i_name = i["name"]
            playlist_names.append(playlist_i_name)
            playlist_tracks = []
            for track_list in i["items"]:
                track_i_name = track_list["track"]["trackName"]
                playlist_tracks.append(track_i_name)
            playlist_dict[playlist_i_name] = playlist_tracks
                
    except:
        print("Error while parsing data. Check for the error.")
    return playlist_dict

#user needs to input the playlist name that they prefer. #this function instantly prints every song in the user's playlist
def playlist_request(playlist_request):
    for name in playlist_names:
        try:
            if name in playlist_request:
                for playlist_name in playlist_dict:
                    if name in playlist_name:
                        global playlist_search
                        playlist_search = {}
                        playlist_search[name] = playlist_dict[name]
        except:
            print(f"Sorry! There is no playlist named {playlist_request} in your library! Please check again and find a valid playlist. Make sure to look for any special characters or spaces in between the words of your playlists")
    return playlist_search
          

            
            