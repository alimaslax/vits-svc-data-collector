from pytube import Playlist

p = Playlist('https://www.youtube.com/playlist?list=OLAK5uy_n4ZCBRWrd7IAA9lR2vIPU-87z09KpjHWg')
# Define the URL of the YouTube playlis

# Iterate over each video in the playlist
for video in p.videos[:17]:
   video.streams.filter(only_audio=True).first().download(output_path=p.title)

print("Download complete!")
