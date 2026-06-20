from etl.transform import clean_movies_data

def test_data_not_empty():
    df = clean_movies_data("data/netflix_titles.csv")
    assert len(df) > 0

def test_no_null_titles():
    df = clean_movies_data("data/netflix_titles.csv")
    assert df["title"].isnull().sum() == 0

def test_columns_exist():
    df = clean_movies_data("data/netflix_titles.csv")
    assert "title" in df.columns
    assert "release_year" in df.columns