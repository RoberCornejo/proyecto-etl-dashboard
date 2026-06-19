def get_movies_for_api(df, limit=10):
    movies_df = df[["title", "release_year"]].head(limit)
    movies = list(movies_df.itertuples(index=False, name=None))
    return movies
