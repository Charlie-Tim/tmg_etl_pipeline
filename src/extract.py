import pandas as pd

def extract_data(file_path: str)  -> pd.DataFrame: 
    '''
    reads csv data and stores in pandas Dataframe with error handling
    args:
        file_path (str): path to hitlog csv file
    returns:
        df (dataframe): pandas dataframe containing the csv data
    '''
    
    try:
    # read csv and store as a pandas dataframe
        df = pd.read_csv(
            file_path,
            dtype={
                'page_name': str,
                'page_url': str,
                'user_id': int
            },
            # read timestamp as UTC datetime
            parse_dates=['timestamp']
        )
    
    # handle exception if the file is missing
    except FileNotFoundError as e:
        print(f"Error: {e}")

    # handle any other exception
    except Exception as e:
        print(f"Error: {e}")
    
    return df

