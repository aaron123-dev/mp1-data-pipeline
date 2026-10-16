import pandas as pd
from src import save_data

def test_save_data_creates_csv(sample_df, tmp_path):
    # TODO: Call save_data() and store its return value.
    # TODO: Assert that the returned path is correct.
    # TODO: Read the saved CSV with pandas.
    # TODO: Assert that its row count and column names match sample_df.

    output_path = tmp_path / "clean.csv"

    return_path = save_data(sample_df, output_path)
    assert return_path == output_path

    df = pd.read_csv(output_path)

    assert len(df) == len(sample_df)
    assert df.columns == sample_df.columns