from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from pytube import YouTube
from os.path import exists
import options



def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


yt_channel = options.channel_name #Change this value to a youtube chanel of your choice
videos = options.videos #The number of videos the download
key = options.key #This is your google api key

#Get the id of the channel from the name
get_id_url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&forUsername={yt_channel}&key={key}"
get_id_page = urlopen(get_id_url)
get_id_html = get_id_page.read().decode("utf-8")
get_id_data = json.loads(get_id_html)

#Store id value from the youtube api
id = get_id_data['items'][0]['id']




page_token = "" #The page token starts at null as it is the first page
result_index = 0 #Add an index to show what video is being accessed

#The api is only able to grab 50 entries at a time, so the program must requery in a loop
for y in range(0,videos/50,1):
    #Get video ids
    video_search_url = f"https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId={id}&maxResults=50&key={key}&pageToken={page_token}"
    page = urlopen(video_search_url)
    html = page.read().decode("utf-8")
    data = json.loads(html)
    for i in range(0,49,1):
        result_index += 1
        video_title = data['items'][i]['snippet']['title']
        video_id = data['items'][i]['id']['videoId']
        
        print(f"{result_index}.")
        print(f"Downloading: {video_title}.mp4")
        print(f"Video id: {video_id}")

        #If the video file doesn't exist download it based on the video id
        if(not exists(video_title + ".mp4")):
            print(f"Url: https://www.youtube.com/watch?v={video_id}")
            try:
                Download(f"https://www.youtube.com/watch?v={video_id}")
            except:
                print("An error occurred (possible video corruption)")
        else:
            print("Video already exists")
        print("\n")

    #Set the new page token for next query
    page_token = data['nextPageToken']



