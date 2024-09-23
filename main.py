import base64
from configparser import ConfigParser

import spotipy as sp
from dotenv import load_dotenv
load_dotenv()

# Load config
config = ConfigParser()
config.read('config.ini')

podfree_dd_name = config.get('SETTINGS', 'NEW_DAILY_DRIVE_NAME')


scopes = ['playlist-read-private',
          'ugc-image-upload',
          'playlist-modify-public',
          'playlist-modify-private']

sp_auth_manager = sp.SpotifyOAuth(scope=scopes, open_browser=False)
sp = sp.Spotify(auth_manager=sp_auth_manager)
user_id = sp.current_user()['id']


def get_daily_drive_id():
    """
    Returns ID of first playlist matching name == "Daily Drive" and author == Spotify
    after searching using Spotifys 'search' endpoint
    :return: ID of first Daily drive match
    """
    dd_candidates = sp.search("Daily Drive", type='playlist')['playlists']['items']
    dd = [*filter(lambda playlist: playlist['name'] == 'Daily Drive' and
                                   playlist['owner']['display_name'] == 'Spotify', dd_candidates)]
    return dd[0]['id']


def get_dd_podfree_id():
    """
    :return: ID of Podfree Daily Drive
    """
    searching = True
    results = sp.current_user_playlists(50)
    while searching:
        filtered_playlists = [*filter(lambda playlist: playlist['name'] == podfree_dd_name, results['items'])]
        if filtered_playlists:
            return filtered_playlists[0]['id']

        if results['next']:
            results = sp.next(results)
            continue
        else:
            return None


def create_dd_podfree():
    """
    Creates Empty Podfree Daily Drive Playlist with name in config
    """
    sp.user_playlist_create(user_id, podfree_dd_name, False, False, '')


def change_cover_img(playlist_id):
    """
    Changes playlist cover of provides playlist to daily drive cover image
    :param playlist_id: ID of targeted playlist
    """
    img_handle = open('daily_drive_cover.jpg', 'rb')
    img_b = img_handle.read()
    img_handle.close()
    sp.playlist_upload_cover_image(playlist_id, base64.b64encode(img_b))


def update_podfree_dd():
    # Retrieve ID of Daily Drive
    dd_id = get_daily_drive_id()

    # Retrieve ID of Podfree Daily Drive
    dd_podfree_id = get_dd_podfree_id()
    if not dd_podfree_id:
        create_dd_podfree()
        dd_podfree_id = get_dd_podfree_id()
        change_cover_img(dd_podfree_id)

    # Retrieve items from original daily drive
    dd_items = sp.playlist_items(dd_id)['items']
    # Filter by track (removing first -> welcome track)
    new_podfree_tracks = [*filter(lambda item: item['track']['track'], dd_items)][1:]
    new_podfree_track_ids = [*map(lambda item: item['track']['id'], new_podfree_tracks)]

    # Clear current podfree daily drive
    current_dd_podfree_items = sp.playlist_items(dd_podfree_id)['items']
    if current_dd_podfree_items:
        current_dd_podfree_ids = [*map(lambda item: item['track']['id'], current_dd_podfree_items)]
        sp.playlist_remove_all_occurrences_of_items(dd_podfree_id, current_dd_podfree_ids)

    # Add new tracks to daily drive
    sp.playlist_add_items(dd_podfree_id, new_podfree_track_ids)


if __name__ == '__main__':
    update_podfree_dd()
