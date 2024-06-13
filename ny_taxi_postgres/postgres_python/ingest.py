import os, sys, argparse
from pathlib import Path
from time import time

import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.tb
    # url = params.url
    data_path = params.data_path
    file_name = params.fp

    
    # # Get the name of the file from url
    # file_name = url.rsplit('/', 1)[-1].strip()
    # print(f'Downloading {file_name} ...')
    # # Download file from url
    # os.system(f"curl {url.strip()} -o {Path(data_path).joinpath(*[file_name])}")
    # print('\n')

    # Create SQL engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Read file based on csv or parquet
    if '.csv' in file_name:
        df = pd.read_csv(f"{Path(data_path).joinpath(*[file_name])}", nrows=10)
        df_iter = pd.read_csv(f"{Path(data_path).joinpath(*[file_name])}", iterator=True, chunksize=100000)
    elif '.parquet' in file_name:
        file = pq.ParquetFile(f"{Path(data_path).joinpath(*[file_name])}")
        df = next(file.iter_batches(batch_size=10)).to_pandas()
        df_iter = file.iter_batches(batch_size=100000)
    else: 
        print('Error. Only .csv or .parquet files allowed.')
        sys.exit()


    # Create the table
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')


    # Insert values
    t_start = time()
    count = 0
    for batch in df_iter:
        count+=1

        if '.parquet' in file_name:
            batch_df = batch.to_pandas()
        else:
            batch_df = batch

        print(f'inserting batch {count}...')

        b_start = time()
        batch_df.to_sql(name=table_name, con=engine, if_exists='append')
        b_end = time()

        print(f'inserted! time taken {b_end-b_start:10.3f} seconds.\n')
        
    t_end = time()   
    print(f'Completed! Total time taken was {t_end-t_start:10.3f} seconds for {count} batches.')    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest data to Postgres')
    # With default setup in .env
    parser.add_argument('--user', default=os.environ.get('user'), help='user name for postgres')
    parser.add_argument('--password', default=os.environ.get('password'), help='password for postgres')
    parser.add_argument('--host', default=os.environ.get('host'), help='host for postgres')
    parser.add_argument('--port', default=os.environ.get('port'), help='port for postgres')
    parser.add_argument('--db', default=os.environ.get('db'), help='database name for postgres')
    parser.add_argument('--data_path', default=os.environ.get('data_path'), help='local path of the data file')
    # Need to enter args in shell command
    # parser.add_argument('--url', required=True, help='url of the data file')
    parser.add_argument('--fp', required=True, help='file path of the data file')
    parser.add_argument('--tb', required=True, help='name of the table where we will write the results to')

    args = parser.parse_args()

    main(args)