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


from VideoDownloader import VideoDownloader
from VideoGenerator import VideoGenerator

import argparse



parser = argparse.ArgumentParser(description="parameters to pass into the music video generator")

#Required Arguments
parser.add_argument("--audio_file", type=str, help="path to the the mp3 file that is used to make the video", action="store", required=True)
parser.add_argument("--output_file", type=str,  help="path to the output mp4 file", action="store", required=True)
parser.add_argument("--search_terms_input", type=str,  help="path to your search terms input file", action="store", required=True)

#Non required arguments
parser.add_argument("--video_directory", type=str,  help="write the arguments")
parser.add_argument("--max_length", type=int,  help="max length of the input files")
parser.add_argument("--sample_rate", type=int,  help="sample rate of your song")
parser.add_argument("--num_vids", type=int,  help="number of videos to download")
parameters = vars(parser.parse_args())

print(parameters)

class MusicVideoGeneratorDriver:
    def __init__(self,
                 audio_file = '',
                 video_directory='outputs',
                 output_file = 'output.mp4',
                 max_length = 360,
                 search_terms_input = 'search.txt',
                 num_vids = 20,
                 sample_rate = None):

        self.VideoDownloaderParams= {
                        'num_vids': num_vids,
                        'max_length': max_length,
                        'search_terms_input': search_terms_input
                      }

        self.VideoMakerParams= {
                        'audio_file': audio_file,
                        'video_directory': video_directory,
                        'output_file': output_file,
                        'num_vids': num_vids,
                        'sample_rate': sample_rate,
                      }
    def execute(self):
        print('Downloading Videos')
        VideoDownloader(**self.VideoDownloaderParams).download_videos()
        print('Creating Music Video')
        VideoMaker(**self.VideoMakerParams).execute()


MusicVideoGeneratorDriver(**parameters).execute()
