import pandas as pd

def load_data(df: pd.DataFrame, save_path: str):
    '''
    writes final output to csv file
    args:
        df (dataframe): pandas dataframe containing the transformed data
        save_path (str): path to save the csv file
    returns:
        None
    '''

    df.to_csv(save_path, index=False)
    print('Data successfully written to csv file')
    
    return
