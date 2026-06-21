import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from transform import clean_movies_data
from extract import get_movies_for_api
from api.api import get_movie_data


NETFLIX_PATH = "data/netflix_titles.csv"
OUTPUT_PATH = "data/movies_final.csv"


def run_etl(limit=50):
    print("Iniciando ETL...")

    netflix_df = clean_movies_data(NETFLIX_PATH)
    print("Películas limpias:", len(netflix_df))

    movies = get_movies_for_api(netflix_df, limit=limit)

    omdb_results = []

    for title, year in movies:
        result = get_movie_data(title, year)

        if result:
            omdb_results.append(result)
            print(f"Encontrada: {title} ({year})")
        else:
            print(f"No encontrada: {title} ({year})")

    omdb_df = pd.DataFrame(omdb_results)

    netflix_df["release_year"] = netflix_df["release_year"].astype(str)
    omdb_df["year"] = omdb_df["year"].astype(str)

    final_df = netflix_df.merge(
        omdb_df,
        left_on=["title", "release_year"],
        right_on=["title", "year"],
        how="inner"
    )

    final_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")

    print("ETL finalizado.")
    print("Dataset final guardado en:", OUTPUT_PATH)
    print("Registros finales:", len(final_df))


if __name__ == "__main__":
    run_etl(limit=300)