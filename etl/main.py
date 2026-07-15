import sys
import os
import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from transform import clean_movies_data
from extract import get_movies_for_api
from api.api import get_movie_data


NETFLIX_PATH = "data/netflix_titles.csv"
OUTPUT_PATH = "data/movies_final.csv"


def run_etl(limit=50):

    print("===================================")
    print("INICIANDO ETL")
    print("===================================")

    netflix_df = clean_movies_data(NETFLIX_PATH)

    print("Películas limpias:", len(netflix_df))

    movies = get_movies_for_api(
        netflix_df,
        limit=limit
    )

    omdb_results = []

    for title, year in movies:

        try:

            result = get_movie_data(title, year)

            if result:

                omdb_results.append(result)

                print(
                    f"Encontrada: {title} ({year})"
                )

            else:

                print(
                    f"No encontrada: {title} ({year})"
                )

        except Exception as e:

            print(
                f"Error consultando {title} ({year}): {e}"
            )

    print("\n===================================")
    print("RESUMEN CONSULTAS OMDB")
    print("===================================")

    print(
        "Registros recuperados:",
        len(omdb_results)
    )

    if len(omdb_results) == 0:

        print(
            "ERROR: No se recuperó ningún registro desde OMDb"
        )

        return

    omdb_df = pd.DataFrame(omdb_results)

    print("\nColumnas encontradas:")

    print(
        omdb_df.columns.tolist()
    )

    print("\nPrimeros registros:")

    print(
        omdb_df.head()
    )

    netflix_df["release_year"] = (
        netflix_df["release_year"]
        .astype(str)
    )

    # Detectar automáticamente el nombre de la columna año

    year_col = None

    for candidate in [
        "year",
        "Year",
        "release_year"
    ]:

        if candidate in omdb_df.columns:

            year_col = candidate
            break

    if year_col is None:

        print(
            "\nERROR: No existe una columna de año en los datos OMDb"
        )

        print(
            "Columnas disponibles:"
        )

        print(
            omdb_df.columns.tolist()
        )

        return

    omdb_df[year_col] = (
        omdb_df[year_col]
        .astype(str)
    )

    # Detectar columna título

    title_col = None

    for candidate in [
        "title",
        "Title"
    ]:

        if candidate in omdb_df.columns:

            title_col = candidate
            break

    if title_col is None:

        print(
            "\nERROR: No existe una columna de título en los datos OMDb"
        )

        print(
            omdb_df.columns.tolist()
        )

        return

    final_df = netflix_df.merge(
        omdb_df,
        left_on=["title", "release_year"],
        right_on=[title_col, year_col],
        how="inner"
    )

    print("\n===================================")
    print("MERGE FINAL")
    print("===================================")

    print(
        "Registros finales:",
        len(final_df)
    )

    if len(final_df) == 0:

        print(
            "ADVERTENCIA: El merge no produjo registros"
        )

        return

    final_df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8"
    )

    print("\nETL FINALIZADO")

    print(
        f"Dataset generado: {OUTPUT_PATH}"
    )

    print(
        f"Filas guardadas: {len(final_df)}"
    )


if __name__ == "__main__":
    run_etl(limit=300)