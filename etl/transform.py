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

def merge_netflix_omdb(netflix_df, omdb_df):
    netflix_df["release_year"] = netflix_df["release_year"].astype(str)
    omdb_df["year"] = omdb_df["year"].astype(str)

    final_df = netflix_df.merge(
        omdb_df,
        left_on=["title", "release_year"],
        right_on=["title", "year"],
        how="inner"
    )

    return final_df


def clean_omdb_columns(df):

    if "runtime" in df.columns:
        df["runtime_minutes"] = (
            df["runtime"]
            .str.replace(" min", "", regex=False)
        )

        df["runtime_minutes"] = pd.to_numeric(
            df["runtime_minutes"],
            errors="coerce"
        )

    if "box_office" in df.columns:
        df["box_office_numeric"] = (
            df["box_office"]
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
        )

        df["box_office_numeric"] = pd.to_numeric(
            df["box_office_numeric"],
            errors="coerce"
        )

    if "imdb_votes" in df.columns:
        df["imdb_votes_numeric"] = (
            df["imdb_votes"]
            .str.replace(",", "", regex=False)
        )

        df["imdb_votes_numeric"] = pd.to_numeric(
            df["imdb_votes_numeric"],
            errors="coerce"
        )

    if "imdb_rating" in df.columns:
        df["imdb_rating"] = pd.to_numeric(
            df["imdb_rating"],
            errors="coerce"
        )

    return df