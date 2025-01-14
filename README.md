
# YouTube Music Playlist Tools

This project includes scripts for managing and importing playlists between Spotify and YouTube Music. The current functionality includes:
1. Randomizing YouTube Music playlists (`randomizer` script).
2. Importing Spotify playlists to YouTube Music and displaying them in sorted order (`importer` script).

---

## Prerequisites

Before you start, make sure you have:
- **Python 3** installed on your system (version 3.7+ recommended).
- `pip` or `pipx` installed for package management.
- `spotipy` and `ytmusicapi` Python libraries installed (see installation steps below).
- Access to **YouTube Music** via a browser (you need your session cookies for authentication).
- Access to **Spotify** - A Spotify Developer account to obtain API credentials.

---

### Installation Steps

#### Step 1: Clone the repository
```bash
git clone https://github.com/dumitrub98/youtubemusictools.git
cd youtubemusictools
```

#### Step 2: Create a virtual environment (optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install dependencies
Install the python libraries:
```bash
pip install ytmusicapi spotipy
```

---

## YouTube MusicAuthentication Setup

To allow the script to interact with your YouTube Music account, you need to provide your session cookies manually:

### Step 1: Open YouTube Music
1. Open [https://music.youtube.com](https://music.youtube.com) in Firefox (or any other browser which allows to export headers in raw format).
2. Log in to your YouTube Music account.

### Step 2: Open Developer Tools
1. Press **F12** or **Ctrl+Shift+I** (Windows/Linux) or **Cmd+Opt+I** (macOS) to open Developer Tools.
2. Navigate to the **Network** tab.

### Step 3: Capture a Request
1. Refresh the page by pressing **F5**.
2. Look for a request named **browse** or **search** in the list.
3. Click on the request and select the **Headers** tab.

### Step 4: Copy Request Headers
1. Scroll to the section **Request Headers**.
2. Copy the full headers, including the `User-Agent`, `Cookie`, and other necessary fields in raw format.

### Step 5: Create `headers.txt`
1. Create a file named `headers.txt` in your project folder.
2. Paste the copied request headers in the following format:
   ```raw
    POST /youtubei/v1/browse?prettyPrint=false HTTP/3
    Host: music.youtube.com
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0
    Accept: */*
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate, br, zstd
    Content-Type: application/json
    Content-Length: 3228
    .....
   ```


### Step 6: Set current session for `ytmusicapi`
```bash
ytmusicapi browser < headers.txt
```

---

## 1. Randomizer Script

This script allows you to randomize the order of tracks in a YouTube Music playlist by removing all tracks and adding them back in a randomized order. It also removes duplicate tracks based on the name and artist.

### How to Run the Script


```bash
python3 randomiser.py <playlist_id> <limit>
```
- `<playlist_id>`: The ID of the YouTube Music playlist (found in the playlist URL).
- `<limit>`: The maximum number of tracks to process (optional, default is `2000`).

### Example:
```bash
python3 randomiser.py "SD110d2d2-djh181d19d81h2d2" 1000
```

#### Output: 
```bash
Randomizing playlist 'My Songs' with 641 tracks.
Removing all tracks from the playlist in batches...
Removing batch 1/4 with 200 tracks...
Removing batch 2/4 with 200 tracks...
Removing batch 3/4 with 200 tracks...
Removing batch 4/4 with 41 tracks...
Adding shuffled tracks to the playlist...
Playlist 'My Songs' has been updated with a randomized order!
```

---

## 2. Importer Script

The importer script transfers playlists from Spotify to YouTube Music and removes duplicates while displaying the final sorted list.

### How to Run the Script

1. Make sure your Spotify API credentials (`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REDIRECT_URI`) are set as environment variables.
  ```bash
   export SPOTIFY_CLIENT_ID="your_spotify_client_id"
   export SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
   export SPOTIFY_REDIRECT_URI="http://localhost:8888/callback/"
   ```

2. Run the importer script with the following command:
   ```bash
   python3 importer.py <spotify_playlist_url> [youtube_music_playlist_id]
   ```
   - `<spotify_playlist_url>`: The URL of the Spotify playlist you want to transfer.
   - `[youtube_music_playlist_id]`: (Optional) The ID of an existing YouTube Music playlist to which tracks will be added.

### Example Output
```bash
Adding 1205 tracks to YouTube Music playlist...
Added 1 of 1205: Through the Fire and Flames - DragonForce
...
Transfer complete!
Removing 15 duplicate tracks...
```

## Important Notes

### Randomizer
- The YT Music playlist must be created by **you**; public or autogenerated playlists cannot be modified.
- The authentication `browser.json` file contains session cookies—keep it secure to avoid unauthorized access.
- If you encounter rate limits from YouTube Music, try reducing the batch size in the script or adding a longer delay.

### Importer
- The script function __display_sorted_tracks__ sorts tracks by **artist name** first and then by **track 
- Duplicate tracks (same artist and track name) are automatically removed.
- You can use `ytmusicapi browser` to generate the `browser.json` file for YouTube Music authentication.
---

## Troubleshooting

- **"Cannot remove songs, because setVideoId is missing":**
  - Make sure you are using a playlist you created.
  - Ensure the authentication `browser.json` is valid.
  
- **"HTTP 401 Unauthorized":**
  - Your session may have expired. Re-export `cookies.txt` and regenerate `browser.json`.

---

## Contributing

Feel free to submit issues or contribute improvements to this project.

---

## Acknowledgements
- Special thanks to the [ytmusicapi](https://github.com/sigma67/ytmusicapi) project for providing an excellent API for interacting with YouTube Music.
- Special thanks to the [spotipy](https://github.com/spotipy-dev/spotipy) project for providing an excellent API for interacting with Spotify.

