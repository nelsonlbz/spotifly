# * ====== IMPORT ====== *
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# * ====== SPOTIFY API FUNCTIONS ====== *
def spotify_auth(client_id, client_secret, uri):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri=uri,
            client_id=client_id,
            client_secret=client_secret,
            show_dialog=True,
            cache_path="token.txt"
        )
    )
    return sp
