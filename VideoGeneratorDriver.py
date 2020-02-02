import argparse

parser = argparse.ArgumentParser()
parser.add_argument("audiofile", help="write the ")




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
        
        
MusicVideoGeneratorDriver(**{'audio_file': 'killers.mp3', 'num_vids': 30}).execute()