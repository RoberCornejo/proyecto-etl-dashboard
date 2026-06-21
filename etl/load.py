import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def load_movies_to_supabase(csv_path="data/movies_final.csv"):
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    df = pd.read_csv(csv_path)

    df = df.rename(columns={
        "director_x": "director_netflix",
        "director_y": "director_omdb",
        "cast": "cast_names"
    })

    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    records = df.to_dict(orient="records")

    response = supabase.table("movies_final").insert(records).execute()

    print("Carga completada en Supabase")
    print("Registros cargados:", len(records))

    return response


if __name__ == "__main__":
    load_movies_to_supabase()