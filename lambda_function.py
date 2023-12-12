import os
import json
import boto3
import uuid
import openai

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SessionTable')  # Replace with your DynamoDB table name

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.environ['OPENAPI_KEY']

def start_session(transcript):
    # Generate a unique session ID
    session_id = str(uuid.uuid4())

    # Store the session data in DynamoDB
    table.put_item(Item={
        'SessionId': session_id,
        'Transcript': transcript,
        'Context': ''  # Placeholder for any initial context if needed
    })
    
    return session_id
