# 🧹 Daily Drive Cleanup
A little handy script that filters out all podcasts, news etc. from Spotifys Daily Drive and only copies the songs to a seperate playlist.

## ⚙️ Setup
1. Clone this repository (`git clone https://github.com/Tohr01/dailyDriveCleanup`)
2. Install the python requirements listed in the requirements.txt file (`pip3 install -r requirements.txt`)
3. Create an app in the the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)<br>
   If you are not really sure how to setup your app and get your Client ID and Secret watch this [Tutorial](https://www.youtube.com/watch?v=kaBVN8uP358)
5. Create a `.env` file with the following structure
   ```
   SPOTIPY_CLIENT_ID=[SPOTIFY CLIENT ID]
   SPOTIPY_CLIENT_SECRET=[SPOTIFY CLIENT SECRET]
   SPOTIPY_REDIRECT_URI=[REDIRECT URI Example: https://localhost:8888/callback]
   ```
6. (Optional) Change name of new Daily Drive copy in the `config.ini`<br>
   ATTENTION: Make sure it has a unique name s.t. the script can replace the songs
7. Initial run:<br>
   `python3 main.py`
   You will be prompted to open a link in your browser. After granting access using your Spotify account you have to copy the url you've been redirected to and paste it into your terminal.

## 🚀 Running
Generally you want to run the script by executing `python main.py`.<br>
This, however, only updates your filtered Daily Drive once. I recommend setting up a cronjob running every day at 0:10 AM.
