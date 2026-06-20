import requests
import os
from dotenv import load_dotenv

# ✅ Cargar correctamente el .env desde la raíz
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

API_KEY = os.getenv("OMDB_API_KEY")
print("API KEY:", API_KEY)

def get_movie_data(title, year):
    url = "http://www.omdbapi.com/"

    params = {
        "apikey": API_KEY,
        "t": title,
        "y": year
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "year": data.get("Year"),
                "imdb_rating": data.get("imdbRating"),
                "director": data.get("Director"),
                "genre": data.get("Genre")
            }

    return None