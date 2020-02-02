class VideoDownloader:
    def __init__(self,
                 num_vids=20, 
                 max_length=360, 
                 search_terms_input=''):
        
        self.num_vids = num_vids
        with open(search_terms_input, 'r') as r:
            self.search_terms = r.read().split('\n')
        r.close()
    
    def download_videos(self):
        random.shuffle(self.search_terms)
        all_options = [self.collect_videos(x) for x in self.search_terms[:4]]
        list_of_links = reduce(lambda x, y: x + y, all_options)
        print(list_of_links)
        if len(list_of_links) > self.num_vids:
            random.shuffle(list_of_links)
            list_of_links = list_of_links[:self.num_vids]
        for i, item in enumerate(list_of_links):
            print('Downloading', item)
            self.download_video(item)
                       
    def download_video(self, link):
        print('downloading', link)
        ydl_opts = {'format': 'mp4',
                    'noplaylist':'true',
                    'outtmpl': 'outputs/%(title)s-%(id)s.%(ext)s',
                    'forceduration' : 'true',
                    'verbose'  : 'true'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            
    def collect_videos(self, search_term):
        video_request = self.get_video_request(search_term)
        list_of_links = self.video_links_from_search_request(video_request)
        collected_vids = [x for x in list_of_links if self.filter_out_long_vids(x)]
        return collected_vids
        
    
    def filter_out_long_vids(self, link):
        try:  
            return pafy.new(link).length < 3600
        except:
            return False
            
    def video_links_from_search_request(self, html):
        soup = BeautifulSoup(html, "html.parser")
        vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})
        vids = filter(lambda x: 'channel' not in x, vids)
        return [''.join(['http://youtube.com', x['href']]) for x in vids]
    
    def get_video_request(self, search_term):
        query ='https://www.youtube.com/results?search_query="{}"++long+-vlog+-review'.format(search_term)
        r = requests.get(query)
        if r.ok:
            return r.text
        raise Exception('Youtube Search Failed')