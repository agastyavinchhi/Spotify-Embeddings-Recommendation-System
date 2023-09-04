import os
import json
import glob
import pandas as pd
import re
import copy

#to stop opening the file again and again - we can open it once here and make it global (optimize)
def file_open(playlist_name = "playlist1.json"):
    f = open("playlist1.json")
    global data
    data = json.load(f)
    f.close()
    return data

#let us also open the public-playlist dataset found on kaggle.com (https://www.kaggle.com/datasets/siropo/spotify-multigenre-playlists-data?resource=download). 
def file_public():
    global df_list
    df_list = []
    path = "/Users/agastya/Desktop/Spotify-Embeddings-Recommendation-System/public-playlists"
    global all_files
    all_files = glob.glob(path + "/*.csv")
    for file_name in all_files:
        df = pd.read_csv(file_name, index_col = None, header = 0)
        df = df.to_dict("index")
        file_regex_string = re.findall(r"\/([^\/]+)\.csv$", file_name)
        df["playlist_genre"] = file_regex_string[0]
        df_list.append(df)
    return df_list

#this function will parse the public datasets that we have just gathered
def file_public_parse():
    global playlist_public 
    global playlist_public_main
    playlist_public = {} #these turn into open ai embeddings!
    playlist_public_main = {}#these are to find popularity and the artist name along with the track!
    for file_name in all_files:
        file_regex_string = re.findall(r"\/([^\/]+)\.csv$", file_name)
        playlist_public[file_regex_string[0]] = None
        playlist_public_main[file_regex_string[0]] = None 
        all_files_regex.append(file_regex_string[0])
    all_files_regex_copy = copy.deepcopy(all_files_regex)
    print(all_files_regex_copy)
    for playlist_no in range(0,len(df_list)):
        df_list[playlist_no]["playlist_genre"] = all_files_regex_copy[playlist_no]
        all_files_regex_copy.pop(playlist_no)
            
    return df_list  

#     list_counter = 0
#     for playlist in df_list:
#         i = len(playlist)
#         track_name_list = []
#         for track_info_iteration in range(0,i):
#             track_name = playlist[track_info_iteration]["Track Name"]
#             artist_name = playlist[track_info_iteration]["Artist Name"]
#             popularity = playlist[track_info_iteration]["Popularity"]
#             track_name_list.append(track_name)
#         for counter in range(0,list_counter):
#             if counter == list_counter:
#                 playlist_public[file_name] = track_name_list
#                 playlist_public_main[file_name] = {"track_name":track_name, "artist_name":artist_name, "popularity":popularity}
#                 break
#             else:
#                 continue
#         list_counter += 1
#     return playlist_public
            
        

#user needs to input the file name with all their spotify data (default spotify data is given as "playlist1.json"). this function will parse the user data to the format we need it in
def user_data_parse(): 
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
    return playlist_names

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

    
#the variable playlist search can now be changed into word embeddings - a seperate py file will be used to make API calls to OpenAi's word embedding system

            
            