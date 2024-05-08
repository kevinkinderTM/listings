import unidecode
import json
import re

def remove_accents(input_string):
    # Use unidecode to remove accents
    output_string = unidecode.unidecode(input_string)
    return output_string

def keyword_to_title (keyword: str):
    # Capitalize the first word
    keyword = keyword.capitalize()
    return keyword.replace('-', ' ')

def text_to_keyword (input: str):
    input = remove_accents(input)
    input = re.sub(r'[^a-zA-Z0-9]+', '-', input).rstrip('-').lstrip('-')
    input = input.replace('.', '-')
    input = re.sub(r'-+', '-', input)
    return input.replace(' ', '-')

def create_basic_json (keyword: str):
    content = {
        "title": keyword_to_title(keyword)
    }
    return json.dumps(content)

def is_valid_json (json_input: str):
    try:
        json_object = json.loads(json_input)
    except json.JSONDecodeError:
        return False
    return True
def concatenate_strings(input_data):
    if isinstance(input_data, str):  # Check if input_data is a string
        return input_data  # Return the input string as it is
    elif isinstance(input_data, list):  # Check if input_data is a list
        print('FIXED ARRAY')
        return ''.join(input_data)  # Concatenate all strings in the list and return as a single string
    else:
        return ''