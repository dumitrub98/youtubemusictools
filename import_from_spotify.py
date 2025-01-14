import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

# Read Spotify credentials from environment variables
spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback/")  # Default redirect URI

if not spotify_client_id or not spotify_client_secret:
    print("Error: Please set the environment variables SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.")
    sys.exit(1)

# Spotify API scope for reading private playlists
scope = "playlist-read-private"

def get_all_spotify_tracks(sp, playlist_id):
    # Fetch tracks in batches of 100
    tracks = []
    offset = 0
    limit = 100  # Maximum number of tracks per request

    while True:
        response = sp.playlist_items(playlist_id, offset=offset, limit=limit)
        batch_tracks = response['items']
        tracks.extend(batch_tracks)
        if len(batch_tracks) < limit:
            break  # No more tracks to fetch
        offset += limit

    return tracks

def display_sorted_tracks(ytmusic, youtube_music_playlist_id):
    # Get all tracks from the YouTube Music playlist
    playlist = ytmusic.get_playlist(youtube_music_playlist_id, limit=1000)
    sorted_tracks = []

    for track in playlist['tracks']:
        track_name = track['title'].strip()
        artist_name = track['artists'][0]['name'].strip() if track['artists'] else "Unknown Artist"
        sorted_tracks.append((artist_name, track_name))

    # Sort tracks by artist and then by track name
    sorted_tracks.sort()

    print("\nSorted Playlist (Artist - Track):")
    for artist, track in sorted_tracks:
        print(f"{artist} - {track}")

def remove_duplicates_from_playlist(ytmusic, youtube_music_playlist_id):
    # Get all tracks in the YouTube Music playlist
    playlist = ytmusic.get_playlist(youtube_music_playlist_id, limit=2000)
    unique_tracks = set()  # To store unique (track_name, artist_name) pairs
    duplicate_track_items = []  # To store duplicate tracks

    for track in playlist['tracks']:
        track_name = track['title'].strip().lower()
        artist_name = track['artists'][0]['name'].strip().lower() if track['artists'] else "unknown artist"
        print(f"Track: {artist_name} - {track_name} ")
        track_key = (track_name, artist_name)

        if track_key in unique_tracks:
            duplicate_track_items.append({"videoId": track['videoId'], "setVideoId": track['setVideoId']})
        else:
            unique_tracks.add(track_key)

    # Remove duplicates
    if duplicate_track_items:
        print(f"Removing {len(duplicate_track_items)} duplicate tracks...")
        ytmusic.remove_playlist_items(youtube_music_playlist_id, duplicate_track_items)
    else:
        print("No duplicates found!")

def transfer_spotify_to_youtube_music(spotify_playlist_url, youtube_music_playlist_id=None):
    # Initialize Spotify API client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                    client_secret=spotify_client_secret,
                                                    redirect_uri=spotify_redirect_uri,
                                                    scope=scope))

    # Extract the Spotify playlist ID from the URL
    playlist_id = spotify_playlist_url.split("/")[-1].split("?")[0]

    # Fetch all tracks from the Spotify playlist
    spotify_tracks = get_all_spotify_tracks(sp, playlist_id)
    track_names = [track['track']['name'] + " - " + track['track']['artists'][0]['name'] for track in spotify_tracks]

    # Authenticate YTMusic
    ytmusic = YTMusic("browser.json")

    # Create a new YouTube Music playlist if no playlist ID is provided
    if youtube_music_playlist_id is None:
        playlist_title = input("Enter the title for the new YouTube Music playlist: ")
        youtube_music_playlist_id = ytmusic.create_playlist(playlist_title, "Imported from Spotify")

    # display_sorted_tracks(ytmusic, youtube_music_playlist_id) # For debugging

    # Add tracks to the specified YouTube Music playlist
    total_tracks = len(track_names)
    print(f"Adding {total_tracks} tracks to YouTube Music playlist...")
    for index, track_name in enumerate(track_names, start=1):
        search_results = ytmusic.search(track_name, "songs")
        if search_results:
            track_id = search_results[0]["videoId"]  # First search result assumed to be correct
            ytmusic.add_playlist_items(youtube_music_playlist_id, [track_id])
            print(f"Added {index} of {total_tracks}: {track_name}")
        else:
            print(f"Warning: Track '{track_name}' not found in YouTube Music")

    print("Transfer complete!")

    # Remove duplicates from the playlist
    remove_duplicates_from_playlist(ytmusic, youtube_music_playlist_id)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print('$ export SPOTIFY_CLIENT_ID="your_spotify_client_id"')
        print('$ export SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"')
        print('$ export SPOTIFY_REDIRECT_URI="http://localhost:8888/callback/"')
        print("$ python script.py <spotify_playlist_url> [youtube_music_playlist_id]")
        sys.exit(1)

    spotify_playlist_url = sys.argv[1]  # First argument: Spotify playlist URL
    youtube_music_playlist_id = sys.argv[2] if len(sys.argv) > 2 else None  # Optional second argument: YouTube Music playlist ID
    
    transfer_spotify_to_youtube_music(spotify_playlist_url, youtube_music_playlist_id)