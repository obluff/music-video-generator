## Generate Music Videos For Great Fun!
* Scrapes youtube for videos and then stiches them together at random onsets in the song.
* Original code and concept by [kihs](https://github.com/kihs)

### Comand Line Arguments
```
  --audio_file AUDIO_FILE
                        path to the the mp3 file that is used to make the video (required)
  --output_file OUTPUT_FILE
                        path to the output mp4 file (required)
  --search_terms_input SEARCH_TERMS_INPUT
                        path to your search terms input file (required)
  --video_directory VIDEO_DIRECTORY
                        write the arguments
  --max_length MAX_LENGTH
                        max length of the input files
  --sample_rate SAMPLE_RATE
                        sample rate of your song
  --num_vids NUM_VIDS   number of videos to download
```

### Example 
```
python src/VideoGeneratorDriver.py  --audio_file "gangsta.mp3" 
                                    --output_file "vibez.mp4" 
                                    --search_terms_input "search.txt"
```

