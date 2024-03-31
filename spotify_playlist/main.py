import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

destination_url = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(destination_url)
website_data = response.text

soup = BeautifulSoup(website_data, 'html.parser')
titles_links = soup.select("li> h3")

titles_list = [title.getText().strip() for title in titles_links]
# print(titles_list[:100])
top_100 = titles_list[:100]

spotify_client_id = "94244f3b40d04cbab56322d82b563e0f"
spotify_client_secret = "01939e3d779045c8bad479bd414ebfa4"
spotify_user_name = "31h7zdiue5ye2kckrkee6uhg4hna"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in top_100:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=spotify_user_name, name=f"{date} Top 100 Billboard", public=False, description=f"Top 100 songs from {date}")
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)