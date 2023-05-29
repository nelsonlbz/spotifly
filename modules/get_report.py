# * ====== IMPORT ====== *
from modules import get_logger
import os
import csv

# * ====== LOGGER ====== *
logger = get_logger.logger_initializer()

# * ====== REPORT CREATION ====== *
def initialize_report(args, playlist_name):
    file_path = f'{args.DOWNLOAD_PATH}/{playlist_name}.csv'
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Spotify_track', 'Downloaded_file', 'Downloaded_date', 'Bitrate'])
        return file_path