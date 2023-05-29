# * ====== SPOTIFY FUNCTIONS ====== *

# * ====== IMPORT ====== *
from modules import get_logger

# * ====== LOGGER ====== *
logger = get_logger.logger_initializer()

# * ====== SPOTIFY ====== *
def get_playlist_uris(playlist_link: str) -> str:
    # This function returns the uris of the spotify playlist:
    playlist_URIs = playlist_link.split("/")[-1].split("?")[0]
    logger.info(f'Playlist URIS: {playlist_URIs}')
    return playlist_URIs


def get_song_details_from_playlist(spotify_auth, playlist_URIs: str) -> dict:
    # This function returns the details of all tracks from the spotify playlist:
    logger.info(f'...Searching for all tracks from the playlist')
    song_details = {}

    for track in spotify_auth.playlist_tracks(playlist_URIs)["items"]:
        # Track details from Spotify
        track_id = track["track"]["id"]
        track_name = track["track"]["name"]
        artist_name = track["track"]["artists"][0]["name"]
        track_uri = track["track"]["uri"]
        
        # Create a new dictionary with relevant informations
        song_details[track_id] = {'artist_name': artist_name,
                                  'track_name': track_name,
                                  'duration': spotify_auth.audio_features(track_uri)[0]['duration_ms'],
                                  'spotify_link': f'https://open.spotify.com/track/{track_id}?si={track_id}',
                                  'search_query': f'{artist_name} {track_name}'}
    return song_details


def get_playlist_name(spotify_auth, client_id, playlist_id) -> str:
    # doc: Get the playlist name:
    
    results = spotify_auth.user_playlist(user=client_id, 
                                         playlist_id=playlist_id, 
                                         fields="name")
    return results["name"]