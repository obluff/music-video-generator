from bs4 import BeautifulSoup
import youtube_dl
import requests
from functools import reduce
import random
import pafy 
import random
import os 
from aubio import source, onset
from moviepy import editor


class VideoGenerator:
    def __init__(self, 
                 audio_file = '', 
                 video_directory='outputs',
                 output_file = 'output.mp4',
                 num_vids = 20, 
                 sample_rate = None):
                 
        self.audio_file = audio_file
        self.num_vids = num_vids
        self.video_directory = video_directory
        self.sample_rate = sample_rate 
        self.output_file = output_file
        
    def execute(self):
        onset_list = remove_random_onsets(get_onset(self.audio_file))
        clip_objs = load_clips(self.video_directory, self.num_vids) 
        final_list = cut_clips(clip_objs, onset_list, 20)
        final_clip = editor.concatenate_videoclips(final_list, method='compose')
        final_clip.write_videofile(self.output_file, audio=self.audio_file)       
        
    def get_onset(self, audio_file, sample_rate=44100):   
        win_s = 512                 # fft size       
        hop_s = win_s // 2          # hop size                
     
        s = source(audio_file, sample_rate, hop_s)
        sample_rate = s.samplerate
        o = onset("default", win_s, hop_s, sample_rate)
     
        # list of onsets, in samples
        onsets = []
        # total number of frames read
        saples, read = s()
        
        total_frames = 0
        while True:
            samples, read = s()
            if o(samples):
                f = "%f" % o.get_last_s()
                onsets.append(f)
            total_frames += read
            if read < hop_s: break
        return [float(x) for x in onsets]
     
    def remove_random_onsets(self, onsets, pct_to_remove=.95):
        idx_to_remove = int(len(onsets) * pct_to_remove)
        random.shuffle(onsets)
        return sorted(onsets[idx_to_remove:])
 
    def load_clips(self, clip_dir, num_vids):
        clips = [x for x in os.listdir(clip_dir) if x.endswith('.mp4')]
        print(clips)
        random.shuffle(clips)
        return [editor.VideoFileClip('/'.join([clip_dir, path])) for path in clips]
 
    def cut_clips(self, clip_objects, onsets, num_vids):
        subclip_list = []
        for i in range(len(onsets)-1):
            subclip = random.choice(clip_objects)
            start_time, end_time  = map(float, (onsets[i], onsets[i + 1]))
            if subclip.duration > start_time and subclip.duration > end_time:
                subclip = subclip.subclip(start_time, end_time)
                subclip_list.append(subclip)
        return subclip_list
  
    