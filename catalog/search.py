import requests
import threading
import queue
import time

base_url = 'https://virtual-catalog.tiendamia.net/api/v2/'

def search_request_first_page_results(keyword):
    data = {
        "search_term": f"{keyword}",
        "merchant_id": "amz",
        "clear_cache": False,
        "navigation_url": "",
        "store": "CR"
    }
    try:
        response = requests.post(f"{base_url}search", data=data)
        if response.status_code == 200:
            response_body = response.json()
            if 'results' in response_body:
                return {'keyword': keyword, 'count': len(response_body['results'])}
            else:
                return {'keyword': keyword, 'count': 'NO_RESULTS_IN_BODY'}
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            return {'keyword': keyword, 'count': 'REQ_ERROR'}
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {'keyword': keyword, 'count': 'REQUEST_EXCEPTION'}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {'keyword': keyword, 'count': 'UNEXPECTED_ERROR'}

def multi_process_keyword(unique_keywords):
    max_threads = 100
    results_queue = queue.Queue()
    threads = []
    for index, keyword in enumerate(unique_keywords):
        thread = threading.Thread(target=process_keyword, args=(keyword, results_queue, index))
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
    return results

def process_keyword(keyword, results_queue, index):
    result = search_request_first_page_results(keyword)
    results_queue.put(result)
    print(f"finished item {index}")