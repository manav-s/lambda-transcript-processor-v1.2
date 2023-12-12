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

def ask_question(transcript, question):
    # Combine the transcript and the question to form the prompt
    prompt = f"{transcript}\n\n{question}"
    
    # Send the prompt to OpenAI's GPT-3.5-turbo-1106 model
    gpt_response = openai.Completion.create(
        engine="text-davinci-003",  # Replace with your chosen model
        prompt=prompt,
        max_tokens=1024  # Adjust as needed
    )

    # Extract the response text
    answer = gpt_response.choices[0].text.strip()
    
    return answer

