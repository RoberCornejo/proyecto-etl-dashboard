import sys
import os
import pandas as pd

# Permite importar módulos desde la raíz del proyecto
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from transform import clean_movies_data
from extract import get_movies_for_api
from api.api import get_movie_data


file_path = "data/netflix_titles.csv"

# 1. Limpiar dataset Netflix
df = clean_movies_data(file_path)

print("✅ Total películas limpias:", len(df))

# 2. Obtener películas para consultar en OMDb
movies = get_movies_for_api(df, limit=20)

print("\n✅ Películas para consultar en API:")
print(movies)

# 3. Consultar OMDb
omdb_results = []

print("\n✅ Consultando OMDb:")

for title, year in movies:
    result = get_movie_data(title, year)

    if result:
        omdb_results.append(result)
        print(f"✅ Encontrada: {title} ({year})")
    else:
        print(f"❌ No encontrada: {title} ({year})")

# 4. Convertir resultados a DataFrame
omdb_df = pd.DataFrame(omdb_results)

# 5. Guardar resultados
output_path = "data/omdb_results_sample.csv"
omdb_df.to_csv(output_path, index=False, encoding="utf-8")

print(f"\n✅ Resultados guardados en {output_path}")
print("\n✅ Vista previa:")
print(omdb_df.head())