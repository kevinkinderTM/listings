import boto3
import os
from dotenv import load_dotenv  # Import the dotenv package
import json
from utils import stringProcessing

load_dotenv()

# Initialize DynamoDB
endpoint_url = os.getenv('AWS_DYNAMO_ENDPOINT')
region_name = os.getenv('AWS_REGION_NAME')

# Get AWS credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token = os.getenv('AWS_SESSION_TOKEN')

# Create a session with the specified credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=region_name
)

# Connect to DynamoDB using the session
dynamodb = session.resource('dynamodb')

# Select the table
table_name = 'seo_listings'
table = dynamodb.Table(table_name)

def get_listing_by_keyword(k: str):
    try:
        # Query get_item
        response = table.get_item(
            Key={"keyword": k}
        )

        # If found
        if 'Item' in response:
            item = response['Item']
            return item
        else:
            print("Item not found")
            return None
    except Exception as e:
        raise Exception(f"Error fetching from DynamoDB: {e}")
    
def create_listing_by_keyword(k: str, content: str = None):
    try:
        if content is None:
            content = stringProcessing.create_basic_json(k)
        # Check if the item already exists
        # existing_item = get_listing_by_keyword(k)
        # if existing_item:
        #     print("Item already exists.")
        #     return existing_item

        # Item doesn't exist, proceed to create it
        response = table.put_item(
            Item={
                "keyword": k,
                "content": content
            }
        )
        
        print("Item created successfully.")
        return response

    except Exception as e:
        raise Exception(f"Error creating item in DynamoDB: {e}")

def create_listing_batch(items_to_upload):
    try:
        # Use batch_writer to upload items in batches
        with table.batch_writer() as batch:
            for item in items_to_upload:
                batch.put_item(Item=item)

        print("Batch upload completed successfully.")
    except Exception as e:
        raise Exception(f"Error creating items in DynamoDB: {e}")    
# get_listing_by_keyword('repuestos-para-autos')
# create_listing_by_keyword('perfumes-importados')