import random
from moviepy.editor import *
import numpy
import ffmpy
import copy
import sys
from aubio import source, onset

audio_file = "Same Thing.mp3"
NumVids = 20
clip_list = []
subclip_list = []
removeCuts = 400

def get_onset(audio_file):
	win_s = 512                 # fft size
	hop_s = win_s // 2          # hop size

	samplerate = 44100
	if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

	s = source(audio_file, samplerate, hop_s)
	samplerate = s.samplerate

	o = onset("default", win_s, hop_s, samplerate)

	# list of onsets, in samples
	global onsets

	onsets = []

	# total number of frames read
	total_frames = 0
	while True:
	    samples, read = s()
	    if o(samples):
	        f = "%f" % o.get_last_s()
	        onsets.append(f)
	    total_frames += read
	    if read < hop_s: break

            # print(len(onsets))

def random_onset(onsets, removeCuts):  
	'''removes points in the array, will sometimes say array 
	bounds exceeded but it works if u try again'''
	sum = 0
	for i in range(0,removeCuts,1):
		sum = sum +1
		n = random.randint(1,len(onsets))
		if (onsets[n]):
			onsets.remove(onsets[n])

get_onset(audio_file)	
print(len(onsets))	
random_onset(onsets, removeCuts)
print(len(onsets))

def load_clips(NumVids):
	print "Loading clips..."
	for i in range(0, NumVids):
		clip = VideoFileClip('/Users/class2018/Desktop/Projects/mg2/temp/' + str(i)+ '.mp4')
		clip_list.append(clip)
# load_clips(NumVids)

def cut_clips(NumVids,onsets):
    #takes longest, perhaps easier way to do it using less subclips
    print "Cutting clips..."
    for i in range(0,len(onsets)-1):
    	print "YO"
        subclip = random.choice(clip_list)
        startTime = float(onsets[i])
        endTime = float(onsets[i+1]) 
        print startTime,endTime
        print subclip.duration

        if (subclip.duration > startTime) and (subclip.duration > endTime):
            subclip = subclip.subclip(startTime, endTime)
            subclip_list.append(subclip)
            print "ADDED",len(subclip_list)


# get_onset(audio_file)	
# random_onset(onsets, removeCuts)	
load_clips(NumVids)		
cut_clips(NumVids,onsets)

final_clip = concatenate_videoclips(subclip_list,method="compose")
final_clip.write_videofile("output.mp4", audio=audio_file,codec="libx264")
