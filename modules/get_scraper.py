# * ====== ALL SCRAPING FUNCTIONS ====== *

# * ====== IMPORT ====== *
import os
import time
from modules import get_logger
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from modules import get_config
SLEEP_TIME = get_config.read_json('config.json')['config']['SLEEP_TIME']

# * ====== LOGGER ====== *
logger = get_logger.logger_initializer()

# * ====== SCRAPER FUNCTIONS ====== *
def search_for_song(search_bar, query):
    # This function searches the track with the search bar:
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.ENTER)
    
def parse_website_elements(parser, download_url) -> str: 
    # This function parses all needed elements from the website:
    mp3_artist = parser.find('li', {'class': 'list-group-item'}).find('a', {'id': 'navi'}).text.lstrip()
    mp3_song_name = parser.find('li', {'class': 'list-group-item'}).find_all('a', {'id': 'navi'})[1].text.lstrip().rstrip()
    mp3_code = parser.find('ul', {'class': 'dropdown-menu'}).a.attrs['data-stream'].split('/stream/')[1]
    mp3_full_name = f'{mp3_artist} - {mp3_song_name}'
    mp3_url = f'{download_url}{mp3_code}'
    return mp3_full_name, mp3_url
        
def launch_the_download(driver, mp3_url, mp3_full_name, download_path, extension) -> str:
    # This function launches the track download:
    
    # Start the download
    start_time_lp = time.time()
    driver.get(mp3_url)
    logger.info(f'{mp3_full_name} - Download started...')

    # Get the download path
    downloaded_file_path = f'{download_path}{mp3_full_name} {extension}'
    
    # Wait for download ending
    timeout = 1
    timeout_limit = 4
    while os.path.exists(downloaded_file_path) is False:
        
        if timeout < timeout_limit:
            time.sleep(SLEEP_TIME)
            logger.info(f'The file is still downloading.. try: {timeout}/{timeout_limit}')
            timeout += 1
        elif timeout == timeout_limit:
            # Close the website if timeout reached
            logger.warning('Your file took too much time... skipping')
            break

    # Close the website once the download is finished
    if os.path.exists(downloaded_file_path):
        logger.info(f'{mp3_full_name} - Download completed in {round((time.time() - start_time_lp),2)} seconds')
        
    driver.quit()
    return downloaded_file_path