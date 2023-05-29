# * ====== TRACK CHECK ====== *

# * ====== IMPORT ====== *
from modules import get_logger
import music_tag
import os

# * ====== LOGGER ====== *
logger = get_logger.logger_initializer()

# * ====== FUNCTION ====== *
def checking_new_tracks(args, folder_path, playlist_name, search_queries):
    args.logger.info(f'...Checking all existing files in {playlist_name}')

    old_queries = []
    
    if len(os.listdir(folder_path)) != 0:
        for file in os.listdir(folder_path):
            new_file_path = f'{folder_path}/{file}'
            
            try:
                old_query = str(music_tag.load_file(new_file_path)['comment']).split('Spotify file name: ')[1]
            except:
                args.logger.critical(f'...We met a problem with old queries')
            else:
                old_queries.append(old_query)
    else:
        args.logger.info(f'...It looks like there are no tracks in the {playlist_name} folder')
                
    non_common_elements = list(set(old_queries) ^ set(search_queries))
    args.logger.info(f'...We found {len(non_common_elements)} new files to download')
    return non_common_elements