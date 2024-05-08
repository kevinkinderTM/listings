import pandas as pd
from utils import stringProcessing
from db import dynamo
from ai import hugginFace
import json
import requests
import threading
import queue
import time



def generate_content_and_update(keyword, index):
    try:
        listing = dynamo.get_listing_by_keyword(keyword)
        if listing:
            content = json.loads(listing['content'])
            if 'description' not in content:
                ai_response = hugginFace.generate_content_for_keyword(keyword)
                if stringProcessing.is_valid_json(ai_response):
                    ai_response = json.loads(ai_response)
                else:
                    print(f"invalid json {ai_response}")
                if "description" in ai_response and "meta_description" in ai_response:
                    # Update the original object with values from the JSON response
                    ai_desc = stringProcessing.concatenate_strings(ai_response["description"])
                    ai_m_desc = stringProcessing.concatenate_strings(ai_response["meta_description"])
                    content["description"] = ai_desc
                    content["meta_description"] = ai_m_desc
                    dynamo.create_listing_by_keyword(keyword, json.dumps(content))
                    print(f"created AI description for {keyword} on index {index}")
                else:
                    print("missing keys in AI response")
            else:
                description = content["description"]
                if isinstance(description, list):
                    description = stringProcessing.concatenate_strings(description)
                    content['description'] = description
                    dynamo.create_listing_by_keyword(keyword, json.dumps(content))
                print(f"{keyword} already has description")
    except Exception as e:
        print(f"Error updating keyword: {e}")

def multi_generate_content(rows):
    max_threads = 1
    results_queue = queue.Queue()
    threads = []
    for index, row in rows:
        rawKeyword = row.iloc[0]
        keyword = stringProcessing.text_to_keyword(rawKeyword)
        thread = threading.Thread(target=generate_content_and_update, args=(keyword, index))
        threads.append(thread)
        thread.start()

        # Limit the number of concurrent threads
        while threading.active_count() > max_threads:
            time.sleep(0.1) 

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Get results from the queue
    results = []
    while not results_queue.empty():
        results.append(results_queue.get())




def main():
    # TODO SEE TO MAKE PARALLEL REQUESTS
    sheet_url = 'https://docs.google.com/spreadsheets/d/1Iu2-w05zj1C5jrK0X0XyKkuZmCiwlkqbyH66IndzhVY/edit#gid=0'
    csv_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    try:
        df = pd.read_csv(csv_url) 
        rows = df.iterrows()
        multi_generate_content(rows)
        # for index, row in df.iterrows():
        #     rawKeyword = row.iloc[0]
        #     keyword = stringProcessing.text_to_keyword(rawKeyword)
        #     generate_content_and_update(keyword)
        #     print(f"generated index {index}")
    except Exception as e:
        print(e)    

if __name__ == '__main__':
    main()
