from transform import clean_movies_data
from extract import get_movies_for_api

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.api import get_movie_data

file_path = "data/netflix_titles.csv"

# ✅ Transform
df = clean_movies_data(file_path)

print("✅ Total películas limpias:", len(df))

# ✅ Extract
movies = get_movies_for_api(df)

print("\n✅ Películas para API:")
print(movies)

# ✅ Test API
print("\n✅ Test conexión API:")

result = get_movie_data("Titanic", 1997)
print(result)