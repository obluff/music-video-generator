from __future__ import unicode_literals
from pytube import YouTube
import os, urllib, urllib2, random
from pprint import pprint
from bs4 import BeautifulSoup
from mutagen.mp3 import MP3
import pytube
import sys
import youtube_dl
import pafy
from subprocess import call


NumVids = 5
audio_file = "selfish shlohmo rip.mp3"

# print song_duration 

def delete_old(NumVids):
	sum = 0
	for i in range(0, NumVids):
		try:
			os.remove('/Users/class2018/Desktop/PROJECTS/mg2/temp/' + str(sum+i) + '.mp4')
		except OSError:
			pass



def youTubeSearch():
	#better search terms would be good thing. ie: duration, restriction, private, no static vid

	# choose a random dictionary word to search
	global videoChoice
	global vid_pafy
	word_file = "search.txt"
	WORDS = open(word_file).read().splitlines()
	videoSearch = random.choice(WORDS);

	# search for, and randomly select YouTube videos in search
	print "SEARCHING: "+videoSearch+"\n"
	videos = []
	query = urllib.quote(videoSearch)
	url = "https://www.youtube.com/results?search_query=" + query + "++long+-vlog+-review"# music/game/math gives us uninteresting videos, remove from search. (still tweaking this)
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html, "html.parser")
	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
	    videos.append('https://www.youtube.com' + vid['href'])
	# print vid['href']
	videos.pop(0)
	videos = [i for i in videos if not ("channel" in i)] # don't want channels
	videoChoice = random.choice(videos)

	try:
		vid_pafy = pafy.new(videoChoice)
		
	except Exception:
		youTubeSearch()
	vid_duration = vid_pafy.length
	print vid_duration
	# print "YOUTUBE SEARCH: Downloading "+videoChoice+"\n"
	song_duration = MP3(audio_file)info.length
	if vid_duration < song_duration or vid_duration > 3600:
		youTubeSearch()


	return videoChoice

# def downloadVideo(NumVids):
# 	'''Pytube's a lil outdated, i have a version that runs youtube-dl thats a lil cleaner
# 	it's important that the vids are longer than the audio otherwise ffmpeg will freak out.
# 	could probably be a lil more robust where it doesn't make cuts'''
# 	delete_old(NumVids)
# 	sum = 0
# 	for i in range(0, NumVids):
# 		youTubeSearch()
# 		ydl_opts = {
# 				'format': 'mp4',
# 				'noplaylist':'true',
# 				# 'forceduration' : 'true',
# 				'verbose'  : 'true',
# 				'outtmpl': 'temp/' +  str(i) +'.%(ext)s' 
# 		}
		
# 		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# 			try:
# 				ydl.download([videoChoice])
# 				sum + i
# 			except Exceptions:
# 				youTubeSearch()


def downloadVideoNew(i):
	try:
		ydl_opts = {
					'format': 'mp4',
					'noplaylist':'true',
					'forceduration' : 'true',
					'verbose'  : 'true',
					'outtmpl': 'temp/' +  str(i) +'.%(ext)s' 
			}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([videoChoice])	
	except Exception:
		youTubeSearch()

def check_dl():
  # if file isn't there do stuff
  for i in range(0, NumVids):
	if os.path.isfile('/Users/class2018/Desktop/PROJECTS/mg2/temp/' + str(i) + '.mp4'):
		return 
	else:
		youTubeSearch()
		downloadVideoNew(i)
		check_dl()

delete_old(NumVids)
check_dl()
# downloadVideo(NumVids)
