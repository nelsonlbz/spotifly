# Spotify Playlist Downloader

Welcome to Spotify Playlist Downloader! This is a Python script that allows you to download tracks from your Spotify playlist using the Spotify API and a web scraping technique.

# Note: Legal and Ethical Use of the Script

We want to emphasize that the Spotify Playlist Downloader script has been created for educational purposes only. We strongly discourage any illegal activities related to copyright infringement, unauthorized downloading, or distribution of copyrighted content.

The purpose of this script is to demonstrate how to work with the Spotify API and Python web scraping techniques. It is intended to help users understand the process of interacting with the Spotify platform and learn about the integration of APIs in Python.

We believe in respecting intellectual property rights and supporting artists and content creators. It is essential to obtain music through legal channels, such as purchasing or streaming from authorized platforms. Engaging in illegal downloading or distribution of copyrighted content goes against ethical standards and legal regulations.

Please use this script responsibly and in compliance with applicable laws and terms of service.

## Installation

Before starting, please make sure to follow these steps:

1. Download the Google Chrome driver: [Download ChromeDriver](https://chromedriver.chromium.org/downloads). Be sure to download the appropriate driver version according to your Chrome browser version. You can check your Chrome version by opening Google Chrome, clicking on the three dots menu, selecting "Help," and then "About Google Chrome."

2. Obtain your Spotify API credentials:

   - Create a Spotify developer account at [Spotify for Developers](https://developer.spotify.com/dashboard/applications).
   - Create a new project in the Spotify Developer Dashboard to obtain the **Client ID** and **Client Secret** tokens.

3. Make sure your playlist is public on Spotify. The script won't be able to find and download tracks from private playlists.

4. Clone this repository to your local machine or download the code files.

5. Install the required Python packages by running the following command:

```
pip install -r requirements.txt
```

## Configuration

1. Create a configuration file named `config.json` in the project directory.

2. Open the `config.json` file and enter the following details:

```json
{
  "config": {
    "CLIENT_ID": "__YOUR_SPOTIFY_CLIENT_TOKEN_ID__",
    "CLIENT_SECRET": "__YOUR_SPOTIFY_CLIENT_SECRET_TOKEN__",
    "URI": "http://localhost:8888/callback",
    "PLAYLIST_LINK": "__PUT_YOUR_PLAYLIST_URL__",
    "DRIVER_PATH": "__PUT_YOUR_DRIVER_PATH__",
    "DOWNLOAD_PATH": "__PUT_YOUR_DOWNLOAD_FOLDER_PATH__"
  }
}
```

- Replace **YOUR_SPOTIFY_CLIENT_TOKEN_ID** with your Spotify client token ID obtained from the Spotify Developer Dashboard.
- Replace **YOUR_SPOTIFY_CLIENT_SECRET_TOKEN** with your Spotify client secret token obtained from the Spotify Developer Dashboard.
- Replace **PUT_YOUR_PLAYLIST_URL** with the URL of the Spotify playlist you want to download. Make sure it is a public playlist.
- Replace **PUT_YOUR_DRIVER_PATH** with the path to the ChromeDriver executable you downloaded.
- Replace **PUT_YOUR_DOWNLOAD_FOLDER_PATH** with the path to the folder where you want to save the downloaded tracks.

## Usage

Make sure you have completed the installation and configuration steps.

Run the script by executing the following command in the project directory:

```
python main.py
```

The script will start running and display logs in the console. It will initialize the program, authenticate with the Spotify API, fetch track details from the playlist, download the tracks, and process them.

Once the script finishes running, you will find the downloaded tracks in the specified download folder path.

## Download Report

At the end of the execution, the script will generate a download report with statistics. You can find the report in a CSV file named after the playlist in the download folder path.

The download report includes the following columns:

- Spotify_track: The track name from Spotify.
- Downloaded_file: The downloaded file name.
- Downloaded_date: The date and time of the download.
- Bitrate: The bitrate of the downloaded track.
- dl_file_duration: The duration of the downloaded track.

## Note

This script relies on web scraping techniques to download tracks from Spotify. It may be subject to potential changes in the Spotify API or website source code.

Have Fun ;)
