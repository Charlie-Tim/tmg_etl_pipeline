import pandas as pd

"""
The transform step comprises two functions: filter_data() and aggregate_data()
This is to make testing easier
"""

def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    filters data to only include articles that were read before the user registerd
    args:
        df (dataframe): pandas dataframe containing the imported data from the hitlog
    returns:
        filtered_df (dataframe): pandas dataframe containing articles that were read before user registration
    '''
     
    # filter out records where any of the fields is null (assume this is bad data so can be ignored)
    df = df.dropna()

    # identify the first registration for each user
    registration_date = df[df['page_url'].str.contains(r'/registration$')].groupby('user_id')['timestamp'].min().reset_index()
    registration_date = registration_date.rename(columns={'timestamp': 'first_registration_timestamp'})

    # left join with df on user_id
    df = df.merge(registration_date, on='user_id', how='left')

    filtered_df = df[
        # filter out articles that occur after the first registration 
        (df['timestamp'] < df['first_registration_timestamp']) &
        # filter out non-articles
        (df['page_url'].str.contains(r'/articles/'))
    ]

    # only count an article once if the user visits the page multiple times
    filtered_df = filtered_df[['page_name', 'page_url', 'user_id']].drop_duplicates()

    return filtered_df
    
    
def aggregate_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    selects the top 3 most influential articles
    args:
        df (dataframe): pandas dataframe containing filtered data  
    returns:
        top_three_articles (dataframe): pandas dataframe containing the three articles that appear most often in all customer journeys
    '''
    
    # count number of times article appeared in all customer journeys
    article_counts_df = df.groupby(['page_name', 'page_url']).size().reset_index(name='total')

    # order by total and select the top 3 articles
    # if there are multiple articles with the third highest total, show multiple articles
    top_three_articles = article_counts_df.nlargest(3, 'total', keep='all').reset_index(drop=True)

    return top_three_articles

