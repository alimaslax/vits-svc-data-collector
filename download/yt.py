from pytube import Playlist
from pytube import YouTube

singleLink = True
video_url = [
   't8xL9nzOWa0',
]
p = Playlist('playlist?list=PL-S_fsUlNDuwPp3I7-4dx-QqUzyqIonNv')
# Define the URL of the YouTube playlis

if(singleLink):
   # Create a YouTube object
   for link in video_url:
      link = 'https://www.youtube.com/watch?v='+ link
      yt = YouTube(link)
      # Download the audio stream
      audio_stream = yt.streams.filter(only_audio=True).first()
      audio_stream.download()
else:
   # Iterate over each video in the playlist
   for video in p.videos[:16]:
      video.streams.filter(only_audio=True).first().download(output_path=p.title)
   video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Replace with your YouTube video URL

print("Download complete!")
