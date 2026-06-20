import pandas as pd

def clean_movies_data(file_path):
    df = pd.read_csv(file_path)

    # ✅ Filtrar películas
    df = df[df["type"] == "Movie"]

    # ✅ Eliminar duplicados
    df = df.drop_duplicates()

    # ✅ Eliminar nulos críticos
    df = df.dropna(subset=["title", "release_year"])

    # ✅ Limpiar texto
    df["title"] = df["title"].str.strip()

    return df
