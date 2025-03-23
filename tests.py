import pytest
import pandas as pd
from src.extract import extract_data
from src.transform import filter_data, aggregate_data

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
