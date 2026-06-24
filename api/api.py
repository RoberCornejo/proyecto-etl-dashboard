import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "https://www.omdbapi.com/"


def get_movie_data(title, year=None):
    params = {
        "apikey": API_KEY,
        "t": title
    }

    if year:
        params["y"] = int(year)

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return None

    if data.get("Response") != "True":
        return None

    return {
        "title": data.get("Title"),
        "year": data.get("Year"),
        "imdb_id": data.get("imdbID"),
        "rated": data.get("Rated"),
        "runtime": data.get("Runtime"),
        "genre": data.get("Genre"),
        "director": data.get("Director"),
        "actors": data.get("Actors"),
        "language": data.get("Language"),
        "country_omdb": data.get("Country"),
        "awards": data.get("Awards"),
        "imdb_rating": data.get("imdbRating"),
        "imdb_votes": data.get("imdbVotes"),
        "metascore": data.get("Metascore"),
        "box_office": data.get("BoxOffice")
    }