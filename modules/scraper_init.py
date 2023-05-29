# * ====== SCRAPER INITIALIZERS ====== *

# * ====== IMPORT ====== *
from modules import get_logger
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from selenium import webdriver
from modules import get_config

# * ====== CONFIG ====== *
DOWNLOAD_PATH = get_config.read_json('config.json')['config']['DOWNLOAD_PATH']

# * ====== LOGGER ====== *
logger = get_logger.logger_initializer()


# * ====== SCRAPER INITIALIZERS ====== *
def get_driver(driver_path) -> str:
    # Initialize the driver instance:
    
    logger.debug(f'...Creating driver instance from path: {driver_path}')
    driver_path = Service(driver_path)
    option = ChromeOptions()
    option.add_argument('headless')
    option.add_argument('window-size=1920x1080')
    option.add_argument("disable-gpu")
    prefs = {f"download.default_directory" : DOWNLOAD_PATH}
    option.add_experimental_option("detach", True)
    option.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=driver_path, options=option)
    return driver

def get_parser(driver) -> str:
    # Initialize the parser:
    
    logger.debug(f'...Creating parser instance')
    html = driver.page_source
    parser = BeautifulSoup(html, "html.parser")
    return parser