from src.extract import extract_data
from src.transform import filter_data, aggregate_data
from src.load import load_data

file_path = "data/hitlog.csv"
save_path = "data/totals.csv"

def run_pipeline(file_path:str, save_path:str):
    
    try:
        
        # extract
        df = extract_data(file_path)

        # transform
        df = filter_data(df)
        df = aggregate_data(df)

        # load
        load_data(df, save_path)

    except Exception as e:
        print(f'Error occurred: {e}')


if __name__ == "__main__":
    # run pipeline
    run_pipeline(file_path, save_path)