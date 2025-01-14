import sys
import random
from ytmusicapi import YTMusic
import time  # for adding a small delay between batches

def batch_remove_tracks(ytmusic, playlist_id, track_ids_to_remove, batch_size=200):
    for i in range(0, len(track_ids_to_remove), batch_size):
        batch = track_ids_to_remove[i:i + batch_size]
        print(f"Removing batch {i // batch_size + 1}/{-(-len(track_ids_to_remove) // batch_size)} with {len(batch)} tracks...")
        ytmusic.remove_playlist_items(playlist_id, batch)
        time.sleep(1)  # 1-second delay to avoid rate-limiting

def randomize_playlist_in_place(playlist_id, limit):
    ytmusic = YTMusic("browser.json")
    playlist = ytmusic.get_playlist(playlist_id, limit=limit)
    playlist_name = playlist['title']
    tracks = playlist['tracks']

    # Create a backup playlist
    backup_playlist_name = f"{playlist_name}_backup"
    backup_playlist_id = ytmusic.create_playlist(backup_playlist_name, "Backup before randomization")
    backup_track_ids = [track['videoId'] for track in tracks]
    ytmusic.add_playlist_items(backup_playlist_id, backup_track_ids)
    print(f"Backup playlist '{backup_playlist_name}' created with {len(backup_track_ids)} tracks.")

    # Shuffle the tracks
    print(f"Randomizing playlist '{playlist_name}' with {len(tracks)} tracks.")
    random.shuffle(tracks)

    # Prepare the list of tracks with `setVideoId` for deletion
    track_ids_to_remove = [{"videoId": track["videoId"], "setVideoId": track["setVideoId"]} for track in tracks]

    # Remove tracks in batches of 200
    print("Removing all tracks from the playlist in batches...")
    batch_remove_tracks(ytmusic, playlist_id, track_ids_to_remove)

    # Add the shuffled tracks to the playlist
    print("Adding shuffled tracks to the playlist...")
    track_ids_to_add = [track['videoId'] for track in tracks]
    ytmusic.add_playlist_items(playlist_id, track_ids_to_add)

    # Delete the backup playlist after transition
    print(f"Deleting backup playlist '{backup_playlist_name}'...")
    ytmusic.delete_playlist(backup_playlist_id)
    print(f"Backup playlist '{backup_playlist_name}' deleted.")

    print(f"Playlist '{playlist_name}' has been updated with a randomized order!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py <playlist_id> <limit>")
        sys.exit(1)

    playlist_id = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 2000

    try:
        randomize_playlist_in_place(playlist_id, limit)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)