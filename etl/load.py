import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def clean_movies_final(df):
    df = df.rename(columns={
        "director_x": "director_netflix",
        "director_y": "director_omdb",
        "cast": "cast_names"
    })

    df = df.replace(["N/A", "nan", "NaN", ""], None)
    df = df.drop_duplicates()

    text_columns = [
        "country", "country_omdb", "cast_names", "actors",
        "director_netflix", "director_omdb", "genre",
        "listed_in", "language", "awards", "rated",
        "rating", "box_office", "metascore"
    ]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].fillna("Sin información")

    if "imdb_rating" in df.columns:
        df["imdb_rating"] = pd.to_numeric(df["imdb_rating"], errors="coerce")

    if "release_year" in df.columns:
        df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")

    df = df.dropna(subset=["title", "release_year"])

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    return df


def load_movies_to_supabase(csv_path="data/movies_final.csv"):
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env")

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    df = pd.read_csv(csv_path)
    df = clean_movies_final(df)

    records = df.to_dict(orient="records")

    supabase.table("movies_final").insert(records).execute()

    print("Carga completada en Supabase")
    print("Registros cargados:", len(records))
    print("Tabla destino: movies_final")


if __name__ == "__main__":
    load_movies_to_supabase()