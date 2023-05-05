from weaviate import Client
import json
import sys
import time
import os 

def delete_data(client: Client, dest_class: str = None) -> None:
    if dest_class:
        client.schema.delete_class(dest_class)
    else:
        client.schema.delete_all()
    return None

def upload_data_weaviate(client: Client, batch_size: int = 200) -> None:
    file_grandmaster = 'grandmaster_nl_pl_only_plot.json'
    file_master = 'master_nl_pl_only_plot.json'
    file_expert = 'expert_nl_pl_only_plot.json'

    with client.batch as batch:
        batch.batch_size = batch_size
        print('adding data from grandmaster')
        with open(file_grandmaster) as file:
            for code_md_pair in json.load(file):
                property = {
                    'code': code_md_pair['code']
                }
                batch.add_data_object(property, "GrandMasterCode")
        print('successfully added data to GrandMasterCode')
        batch.batch_size = batch_size
        print('adding data from master')
        with open(file_master) as file:
            for code_md_pair in json.load(file):
                property = {
                    'code': code_md_pair['code']
                }
                batch.add_data_object(property, "MasterCode")
        print('successfully added data to MasterCode')
        batch.batch_size = batch_size
        print('adding data from expert')
        with open(file_expert) as file:
            for code_md_pair in json.load(file):
                property = {
                    'code': code_md_pair['code']
                }
                batch.add_data_object(property, "ExpertCode")
        print('successfully added data to ExpertCode')

    return None

def main():
    client = Client("http://localhost:81")
    
    wait_time_limit = 240
    while not client.is_ready():
        if not wait_time_limit:
            sys.stderr.write("\rTIMEOUT: Weaviate not ready. \
                            Try again or check if weaviate is running.\n")
            sys.exit(1)
        sys.stdout.write(
            f"\rWait for weaviate to get ready. {wait_time_limit:02d} seconds left.")
        sys.stdout.flush()
        wait_time_limit -= 2
        time.sleep(2.0)

    # Reset schema
    delete_data(client)

    if not client.schema.contains():
        sys.stdout.write(f'\rThe schema is not found on the server. \nPrepare to create schema.')
        sys.stdout.flush()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        schema_file = os.path.join(dir_path, "schema.json")
        client.schema.create(schema_file)
        print(f'\r\nSuccessfully created schema.')


    print('\rPrepare to import data.')
    upload_data_weaviate(client, batch_size=20)
    print('Successfully importing data.')



if __name__ == '__main__': 
    print(__file__)
    main()
