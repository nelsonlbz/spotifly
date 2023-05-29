# * ====== IMPORT ====== *
import os
from modules import get_logger

# * ====== LOGGER ====== *
logger = get_logger.logger_initializer()

# * ====== FOLDER CREATION ====== *
def create_folder(folder_path, playlist_name) -> str:
    # doc: Create a folder if the folder doesn't exist:
    logger.info(f'...Creating a folder for the playlist')
    
    folder_path = f'{folder_path}{playlist_name}'
    try: 
        if os.path.isdir(folder_path):
            raise FileExistsError
            
    except FileExistsError:
        logger.warning(f'The folder {folder_path} already exists')

    else:
        os.makedirs(folder_path)
        logger.info(f'The folder {folder_path} has been created')

    return folder_path