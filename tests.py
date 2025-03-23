import pytest
import pandas as pd
from src.extract import extract_data
from src.transform import transform_data

"""
tests for extracted data from hitlog file
"""

@pytest.fixture()
def extracted_data():
    extracted_data = extract_data('data/hitlog.csv')
    return extracted_data

def test_extracted_data(extracted_data):
    # check output type
    assert isinstance(extracted_data, pd.DataFrame)

    # confirm only four columns
    assert len(extracted_data.columns) == 4


# confirm there is only data from the past 24 hours
def test_timestamps(extracted_data):
    assert extracted_data['timestamp'].max() - extracted_data['timestamp'].min() < pd.Timedelta(hours=24)




"""
tests for transform code
"""

pytest.fixture()
def transformed_data():
    extracted_data = extract_data('hitlog.csv')
    transformed_data = transform_data(extracted_data)
    return transformed_data

def test_transformed_data(transformed_data):
    # check output type
    assert isinstance(transformed_data, pd.DataFrame), "Output is not a pandas dataframe"
    
    # confirm only three columns
    assert len(transformed_data.columns) == 3, "Number of columns is not as expected"