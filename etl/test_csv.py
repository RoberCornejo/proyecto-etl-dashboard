from transform import clean_movies_data
from extract import get_movies_for_api


file_path = "data/netflix_titles.csv"

# ✅ Transform
df = clean_movies_data(file_path)

print("✅ Total películas limpias:", len(df))

# ✅ Extract
movies = get_movies_for_api(df)

print("\n✅ Películas para API:")
print(movies)