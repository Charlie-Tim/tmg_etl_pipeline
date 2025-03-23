import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    outputs the three most influential articles
    args:
        df (dataframe): pandas dataframe containing the imported data from the hitlog
    returns:
        top_three_articles (dataframe): pandas dataframe containing the three articles that appear most often in all customer journeys
    '''

    # identify the first registration for each user
    registration_date = df[df['page_url'].str.contains(r'/registration')].groupby('user_id')['timestamp'].min().reset_index()
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

    # count number of times article appeared in all customer journeys
    article_counts_df = filtered_df.groupby(['page_name', 'page_url']).size().reset_index(name='total')

    # order by total and select the top 3 articles
    top_three_articles = article_counts_df.nlargest(3, 'total').reset_index(drop=True)

    return top_three_articles
