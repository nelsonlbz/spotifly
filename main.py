# * ====== IMPORT ====== *
from datetime import datetime
import music_tag
import shutil
import string
import time
import csv
import os
import re

# * ====== SELENIUM IMPORT ====== *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

# * ====== MODULES IMPORT ====== *
from modules import scraper_init
from modules import spotify_api
from modules import get_logger
from modules import get_folder
from modules import get_scraper
from modules import get_config
from modules import get_args
from modules import renamer
from modules import spotify
from modules import get_track_check
from modules import get_report

# * ====== LOAD CONFIG ====== *
CONFIG = get_config.read_json('config.json')['config']

# * ====== ARGS INITIALIZATION ====== *
params = {'CLIENT_ID': CONFIG['CLIENT_ID'],
          'CLIENT_SECRET': CONFIG['CLIENT_SECRET'],
          'URI': CONFIG['URI'],
          'PLAYLIST_LINK': CONFIG['PLAYLIST_LINK'],
          'DRIVER_PATH': CONFIG['DRIVER_PATH'],
          'WEBSITE': CONFIG['WEBSITE'],
          'DOWNLOAD_PATH': CONFIG['DOWNLOAD_PATH'],
          'logger': get_logger.logger_initializer()}

args = get_args.quick_initialize_args(**params)


def main(args):
    start_time = time.time()
    EXTENSION = "myfreemp3.vip .mp3"
    DOWNLOAD_URL = "https://speed.idmp3s.com/"
    
    # * ====== REPORT INITIALIZATION ====== *
    downloaded_tracks = not_founded_tracks = time_out_tracks = already_downloaded_tracks = poor_quality_tracks = 0
    
    ## -------> Part I: Initialization
    for link in args.PLAYLIST_LINK:
    
        # (1) Initializing the spotify API)
        args.logger.info(f'...Initializing the program')
        spotify_auth = spotify_api.spotify_auth(args.CLIENT_ID, args.CLIENT_SECRET, args.URI)
        
        # (2) Get the playlist URIs from the Spotify API
        playlist_URIs = spotify.get_playlist_uris(link)
        
        # (3) Get all track details of the Spotify playlist from the Spotify API
        all_song_details = spotify.get_song_details_from_playlist(spotify_auth, playlist_URIs)
        
        # (4) Create a list with all track ids
        song_id_list = list(all_song_details.keys())
        
        # (5) Get the Spotify playlist name from the Spotify API
        playlist_name = spotify.get_playlist_name(spotify_auth, args.CLIENT_ID, link)
        
        # (6) Create a list with all track queries 
        search_queries = [all_song_details[id]['search_query'] for id in song_id_list]
        
        # (7) Create a folder with the playlist name
        folder_path = get_folder.create_folder(args.DOWNLOAD_PATH, playlist_name)
        
        # (8) Filter only not already downloaded files in the folder
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
                
        
        non_common_elements = list(set(old_queries) ^ set(search_queries))
        
        total_tracks = len(non_common_elements)
        args.logger.info(f'...We found {total_tracks} new files to download')
        
        # (9) Create a new csv file containing the downloaded details
        csv_file_path = f'{args.DOWNLOAD_PATH}/{playlist_name}.csv'
        
        if not os.path.exists(csv_file_path):
            args.logger.info(f'...Creating a csv file for the download report: {playlist_name}.csv')
            with open(csv_file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Spotify_track', 'Downloaded_file', 'Downloaded_date', 'Bitrate', 'dl_file_duration'])
        else:
            args.logger.info(f'...We found a csv file: {playlist_name}.csv')
    
        ## -------> Part II: Download
        print('\b')
        args.logger.info(f'>>>>> The playlist {playlist_name} will be downloaded now')
        
        for idx, query in enumerate(non_common_elements, start=1):
            args.logger.info(f'{idx}/{total_tracks} | Track: {query}')

            # (1) Initialize a driver instance
            driver = scraper_init.get_driver(args.DRIVER_PATH)
            
            # (2) Open the website with the driver 
            driver.get(args.WEBSITE)
            
            # (3) Check if the website loaded successfully by trying to parse the search bar 
            try:
                search_bar = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.ID, "query")))
                    
            except TimeoutException:
                args.logger.warning(f"The website did not load successfully: No search bar found!")
                time_out_tracks += 1
            
            else:
                args.logger.info(f"The website has been loaded successfully: Search bar found!")
                
                # (4) Search for full track name on the search bar using a query 
                get_scraper.search_for_song(search_bar, query)
                
                # (5) Check if the track exists on the server by parsing a html element
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "list-group-item-danger")))
                    args.logger.warning(f'The track {query} does not exist on the server!')
                    not_founded_tracks += 1
                    driver.quit()
                    pass

                except TimeoutException:
                    args.logger.info(f'The track {query} exists on the server!')
                    
                    # (6) Initialize a parser instance
                    parser = scraper_init.get_parser(driver)
                    
                    # (7) Parse the website elements, getting the first track found and his download url
                    try:
                        mp3_full_name, mp3_url = get_scraper.parse_website_elements(parser, DOWNLOAD_URL)
                    except AttributeError:
                        args.logger.critical("Timeout Error while loading tracks from the server... skipping tracks")
                        
                    
                    # (8) Check if the track already exists in the playlist folder
                    try:
                        if os.path.exists(f'{args.DOWNLOAD_PATH}{playlist_name}/{mp3_full_name}.mp3'):
                            already_downloaded_tracks += 1
                            driver.quit()
                            raise FileExistsError
        
                    except FileExistsError:
                        args.logger.warning(f'This file {mp3_full_name} already exists in {playlist_name}, skipping tracks...')
                        pass
                        
                    else:
                        args.logger.info(f"This file {mp3_full_name} doesn't exists in {playlist_name} folder, downloading...")
                        
                        # (9) Download the track from the website server
                        downloaded_file_path = get_scraper.launch_the_download(driver, mp3_url, mp3_full_name, args.DOWNLOAD_PATH, EXTENSION)
            
                        ## -------> Part III: Preprocessing
                        
                        # (1) Check if file file has been downloaded and exists in the download folder
                        
                        try:
                            
                            if downloaded_file_path:
                                
                                # (2) Clean the file name, removing website suffix
                                file_dowloaded_name = string.capwords(downloaded_file_path.split('/')[-1].replace(' myfreemp3.vip ', ''))
                                
                                # (2) Create the new file path before moving it
                                new_file_path = f'{args.DOWNLOAD_PATH}{playlist_name}/{file_dowloaded_name}'

                                # (3) Move the file from the old to the new path 
                                shutil.move(downloaded_file_path, new_file_path)

                                # (4) Extract the tracks details: track name, artist, ect..
                                file_name, artist_name, song_name = renamer.get_file_details(new_file_path, playlist_name)
                                
                                # (5) Add metadata to the file using extracted data above
                                meta_title, meta_artist, meta_comment, meta_bitrate, meta_samplerate, meta_duration = renamer.modify_metadata(artist_name, 
                                                                                                                                              song_name, 
                                                                                                                                              new_file_path, 
                                                                                                                                              playlist_name,
                                                                                                                                              query)
                                
                                args.logger.info(f">> Title: {meta_title}")
                                args.logger.info(f">> Artist: {meta_artist}")
                                args.logger.info(f">> Comment: {meta_comment}")
                                args.logger.info(f">> Duration: {meta_duration}")
                                downloaded_tracks += 1
                                
                                # (6) Check the bitrate quality of the track
                                if str(meta_bitrate) == '320000':
                                    args.logger.info(f">> Bitrate: {meta_bitrate} -> Good quality detected")
                                else:
                                    args.logger.warning(f">> Bitrate: {meta_bitrate} -> Poor quality detected")
                                    poor_quality_tracks += 1
                                args.logger.info(f">> Samplerate: {meta_samplerate}")    
                                
                                # (7) Add the downloaded tracks details to the CSV file
                                with open(csv_file_path, 'a', newline='') as csvfile:
                                    csvwriter = csv.writer(csvfile)
                                    csvwriter.writerow([query, file_name, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), meta_bitrate, meta_duration])
                                    
                        except:
                            args.logger.warning('Your track does not exist in the playlist path')
                            time_out_tracks += 1
                            pass
            
            args.logger.info(f'Done - {round((time.time() - start_time),2)} seconds\n' )
            
            
    ## -------> Part IV: Statistics

    # * ====== DOWNLOAD STATISTICS ====== *
        
    args.logger.info('======> DOWNLOAD REPORT <======')
    args.logger.info(f'Tracks downloaded: {downloaded_tracks}')              
    args.logger.info(f'Tracks not founded: {not_founded_tracks}')
    args.logger.info(f'Tracks with time out: {time_out_tracks}')
    args.logger.info(f'Tracks already downloaded: {already_downloaded_tracks}')
    args.logger.info(f'Tracks with poor quality: {poor_quality_tracks}')


if __name__ == '__main__':
    main(args)
    
    