# * ====== RENAMER ====== *

# * ====== IMPORT ====== *
import music_tag
from datetime import date

# * ====== PREPROCESS FUNCTIONS ====== *
def get_file_details(new_file_path, playlist_name):
    file_name = new_file_path.split(f'/{playlist_name}/')[1]
    artist_name = file_name.split(' - ')[0]
    song_name = file_name.split(' - ')[1].replace('.mp3','')
    return file_name, artist_name, song_name

def modify_metadata(artist_name, song_name, new_file_path, playlist_name, query):
    audiofile = music_tag.load_file(new_file_path)
    audiofile['tracktitle'] = song_name
    audiofile['artist'] = artist_name
    comment = f'This track has been downloaded the {date.today().strftime("%d/%m/%y")}, from the playlist: {playlist_name}, Spotify file name: {query}'
    audiofile['comment'] = comment
    audiofile.save()
    return audiofile['tracktitle'], audiofile['artist'], audiofile['comment'], audiofile['#bitrate'], audiofile['#samplerate'], audiofile['#length']

