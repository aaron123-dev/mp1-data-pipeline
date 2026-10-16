#tests/test_data_validator.py

import pytest
from src import validate_dataframe

def test_validate_dataframe_removes_invalid_ratings(sample_df):
    #Arrange: TODO: Set the required and numeric column names
    # TODO: Set the required and numeric column names.
    # TODO: Call validate_dataframe().
    # TODO: Assert that 98 rows remain and all five columns are preserved.

    REQUIRED_COLUMNS = {"record_id", "name", "rating", "category", "status"}
    NUMERIC_COLUMNS = {"rating"}

    validated_df = validate_dataframe(sample_df, REQUIRED_COLUMNS, NUMERIC_COLUMNS)
    
    
    assert len(validated_df) == 98
    assert validated_df.columns.tolist() == REQUIRED_COLUMNS



def test_validate_dataframe_with_missing_column(sample_df):
    # TODO: Set required_columns to include a nonexistent column.
    # TODO: Use pytest.raises(ValueError) around validate_dataframe().

    required_columns = ["rating", "nonexistent column"]

    with pytest.raises(ValueError):
        validate_dataframe(sample_df, required_columns)