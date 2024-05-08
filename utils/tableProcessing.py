import pandas as pd
from catalog import search
from db import dynamo
from utils import stringProcessing

def merge_excel_files(start_index=1, end_index=10, directory='pages/', output_file='final.xlsx'):
    # Initialize an empty DataFrame to hold all the data
    final_df = pd.DataFrame()

    # Loop through the specified range of files
    for i in range(start_index, end_index+1):
        file_name = f'{directory}count_{i}.xlsx'
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_name)
        # Concatenate the DataFrame to the final DataFrame
        final_df = pd.concat([final_df, df])

    # Save the final DataFrame to a new Excel file
    final_df.to_excel(output_file, index=False)
    print(f'Merged {end_index - start_index + 1} files into {output_file}')

def generate_excel_counting_results(csv_url, output_file, page):
    """Read a CSV file from a remote URL, generate unique keywords, and save them to an Excel file."""
    page_size = 10000
    start_index = (page - 1) * page_size
    end_index = page * page_size
    try:
        # Read CSV data into a pandas DataFrame
        df = pd.read_csv(csv_url)

        # Initialize an empty set to store unique keywords
        unique_keywords = set()

        # Generate unique keywords based on CSV data and add to unique_keywords set
        for index, row in df.iterrows():
            if start_index <= index < end_index:
                rawKeyword = row.iloc[0]
                keyword = stringProcessing.text_to_keyword(rawKeyword).lower()
                
                # Check if keyword is already in the set (duplicate check)
                if keyword not in unique_keywords:
                    unique_keywords.add(keyword)
                    print(f"ADD {index} item")

        # Use multithreading to process keywords in parallel
        results = search.multi_process_keyword(unique_keywords)

        # Initialize lists to store keys and values
        keys_list = []
        values_list = []

        # Extract keys and values from each object in the results
        for result in results:
            keys_list.append(result['keyword'])
            values_list.append(result['count'])

        # # Create a DataFrame with keys and values as columns
        dataFrameToSave = pd.DataFrame({'Keys': keys_list, 'Values': values_list}, index=None)

        # Save DataFrame to an Excel file
        dataFrameToSave.to_excel(output_file, index=False)
        print(f"Excel file '{output_file}' created successfully with unique keywords.")
    except Exception as e:
        print(f"Error generating Excel file: {e}")

def process_and_upload_csv(csv_url):
    try:
        # Read the CSV file directly into a pandas DataFrame
        df = pd.read_csv(csv_url)

        # Initialize an empty list to store items for batch upload
        items_to_upload = []

        # Initialize a set to store unique keys
        unique_keys = set()

        # Iterate through rows and create items for batch upload
        for index, row in df.iterrows():
            rawKeyword = row.iloc[0]
            keyword = stringProcessing.text_to_keyword(rawKeyword)
            content = stringProcessing.create_basic_json(keyword)
            item = {
                "keyword": keyword,
                "content": content
            }

            # Check for duplicate keys before adding item to batch
            if item["keyword"] not in unique_keys:
                items_to_upload.append(item)
                unique_keys.add(item["keyword"])
                print(f"Item {index} processed")

                # Perform batch upload when items_to_upload reaches 5000 items
                if len(items_to_upload) == 5000:
                    dynamo.create_listing_batch(items_to_upload)
                    items_to_upload = []  # Reset the list after batch upload

        # Perform final batch upload for remaining items
        if items_to_upload:
            dynamo.create_listing_batch(items_to_upload)

        print("DONE")
    except Exception as e:
        print(f"Error reading CSV file from URL: {e}")

def generate_excel_with_unique_links(csv_url, output_file):
    try:
        # Read CSV
        df = pd.read_csv(csv_url)

        # Initialize an empty set
        unique_keywords = set()

        # Generate unique links based on CSV
        for index, row in df.iterrows():
            rawKeyword = row.iloc[0]
            keyword = stringProcessing.text_to_keyword(rawKeyword)
            keyword = f"https://www.tiendamia.cr/listado/{keyword}"
            
            # Check if keyword is already in the set (duplicate check)
            if keyword not in unique_keywords:
                unique_keywords.add(keyword)
                print(f"ADD {index} item")

        unique_keywords_list = list(unique_keywords)

        dataFrameToSave = pd.DataFrame(unique_keywords_list, columns=['URLs'])

        # Save df_unique_keywords to an Excel file
        dataFrameToSave.to_excel(output_file, index=False)
        print(f"Excel file '{output_file}' created successfully with unique keywords.")
    except Exception as e:
        print(f"Error generating Excel file: {e}")



def batch_upload_to_dynamo(file_path):
    try:
        # Read the file into a DataFrame
        df = pd.read_excel(file_path) 

        items_to_upload = []

        unique_keys = set()


        # Iterate through rows and create items for batch upload
        for index, row in df.iterrows():
            rawKeyword = row['Keys']
            keyword = stringProcessing.text_to_keyword(rawKeyword)
            content = stringProcessing.create_basic_json(keyword)
            item = {
                "keyword": keyword,
                "content": content
            }

            # Check if result not empty
            if int(row['Values']) > 0:
                # Check for duplicate keys before adding item to batch
                if item["keyword"] not in unique_keys:
                    items_to_upload.append(item)
                    unique_keys.add(item["keyword"])
                    print(f"Item {index} processed")

                    # Perform batch upload when items_to_upload reaches 5000 items
                    if len(items_to_upload) == 5000:
                        dynamo.create_listing_batch(items_to_upload)
                        items_to_upload = []  # Reset the list after batch upload

        # Perform final batch upload for remaining items
        if items_to_upload:
            dynamo.create_listing_batch(items_to_upload)

        print("DONE")

        # Print the first few rows of the DataFrame
        for index, row in df.iterrows():
            if index < 10:
                keyword = row['Keys']
                count = int(row['Values'])
                cleanKeyword = stringProcessing.text_to_keyword(keyword)
                if int(count) > 0:
                    print(cleanKeyword)
                # for key, val in row.items():
                #     print(key)
    except Exception as e:
        print(f"Error reading CSV file from URL: {e}")