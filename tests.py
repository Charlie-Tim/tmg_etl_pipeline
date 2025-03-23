import pandas as pd
import pytest
from src.extract import extract_data
from src.transform import filter_data, aggregate_data
from src.load import load_data

"""
tests for extracted data from hitlog file
"""

@pytest.fixture()
def extracted_data():
    extracted_data = extract_data('data/hitlog.csv')
    return extracted_data

def test_extracted_data(extracted_data):
    # check output type
    assert isinstance(extracted_data, pd.DataFrame), "Extracted data is not a dataframe"

    # confirm only four columns
    assert len(extracted_data.columns) == 4, "The number of columns is not as expected"

    # confirm column names
    expected_columns = ["page_name", "page_url", "user_id", "timestamp"]
    assert list(extracted_data.columns) == expected_columns, "Column names are not as expected"

    # confirm column types
    expected_dtypes = ["object", "object", "object", "datetime64[ns]"]
    assert list(extracted_data.dtypes) == expected_dtypes, "Column types are not as expected"

# confirm there is only data from the past 24 hours
def test_timestamps(extracted_data):
    assert extracted_data['timestamp'].max() - extracted_data['timestamp'].min() < pd.Timedelta(hours=24)


"""
tests for transform code
"""

# ensure that an article is only counted once if a user loads the same url multiple times
def test_remove_article_duplicates():
    # sample data
    dummy_data = pd.DataFrame(
        {
        'page_name': ['article1', 'article2', 'article1', 'registration'],
        'page_url': ['https://www.telegraph.co.uk/articles/article1', 'https://www.telegraph.co.uk/articles/article2',
                    'https://www.telegraph.co.uk/articles/article1', 'https://www.telegraph.co.uk/articles/registration'],
        'user_id': [1234, 1234, 1234, 1234],
        'timestamp': ['2024-03-22 10:22:17', '2024-03-22 10:23:18', '2024-03-22 10:24:19', 
                    '2024-03-22 10:36:22']
        }
    )
    
    # ensure that the filtered df returns two records - article1 and article2 (timestamp is no longer relevant)
    filtered_data = filter_data(dummy_data)
    assert len(filtered_data) == 2


# check that if an article includes regristration in its name it is still counted
def test_registration_in_page_url():
    # sample data
    dummy_data = pd.DataFrame(
        {
        'page_name': ['registration numbers decline at top universities', 'registration'],
        'page_url': ['https://www.telegraph.co.uk//articles/registration-numbers-decline-at-top-universities', 'https://www.telegraph.co.uk/articles/registration'],
        'user_id': [1234, 1234],
        'timestamp': ['2024-03-22 10:22:17', '2024-03-22 10:23:18']
        }
    )
    
    filtered_data = filter_data(dummy_data)
    assert filtered_data['page_name'][0] == 'registration numbers decline at top universities'


# check that no records are returned for a customer that doesn't register
def test_articles_for_non_registered_user():
    # sample data
    dummy_data = pd.DataFrame(
        {
        'page_name': ['article1', 'article2', 'article1', 'registration'],
        'page_url': ['https://www.telegraph.co.uk/articles/article1', 'https://www.telegraph.co.uk/articles/article2',
                    'https://www.telegraph.co.uk/articles/article1', 'https://www.telegraph.co.uk/articles/registration'],
        'user_id': [1234, 1234, 5678, 5678],
        'timestamp': ['2024-03-22 10:22:17', '2024-03-22 10:23:18', '2024-03-22 10:24:19', 
                    '2024-03-22 10:36:22']
        }
    )
    
    filtered_data = filter_data(dummy_data)
    assert filtered_data['user_id'].nunique() == 1 and filtered_data['user_id'].iloc[0] == 5678


# if the url is the same but the name of the article changes, count these separately
def test_page_url_change():
    # sample data
    dummy_data = pd.DataFrame(
        {
        'page_name': ['Liverpool suffer gruelling defeat', 'Liverpool title hopes dashed', 'registration'],
        'page_url': ['https://www.telegraph.co.uk/articles/article1', 'https://www.telegraph.co.uk/articles/article1',
                    'https://www.telegraph.co.uk/articles/registration'],
        'user_id': [1234, 1234, 1234],
        'timestamp': ['2024-03-22 10:22:17', '2024-03-22 10:23:18', '2024-03-22 10:24:19']
        }
    )
    
    filtered_data = filter_data(dummy_data)
    assert list(filtered_data['page_name']) == list(dummy_data['page_name'][:2])



"""
tests for transform output from hitlog file
"""

@pytest.fixture()
def transformed_data():
    extracted_data = extract_data('data/hitlog.csv')
    filtered_data = filter_data(extracted_data)
    transformed_data = aggregate_data(filtered_data)
    return transformed_data

def test_transformed_data(transformed_data):
    # check output type
    assert isinstance(transformed_data, pd.DataFrame), "Output is not a pandas dataframe"
    
    # confirm only three columns
    assert len(transformed_data.columns) == 3, "Number of columns is not as expected"

    # confirm column names
    expected_columns = ["page_name", "page_url", "total"]
    assert list(transformed_data.columns) == expected_columns, "Column names are not as expected"

    # confirm column types
    expected_dtypes = ["object", "object", "int"]
    assert list(transformed_data.dtypes) == expected_dtypes, "Column types are not as expected"

def test_top_three(transformed_data):
    # ensure that top three totals are in order
    assert transformed_data['total'].is_monotonic_decreasing, "Column 'total' is not ordered correctly"

    # ensure that if there are more than three articles returned this is due to a tie
    if len(transformed_data) > 3:
        third_value = transformed_data.loc[2, 'total']
        assert (transformed_data.loc[2:, 'total'] == third_value).all(), "Too many articles returned"