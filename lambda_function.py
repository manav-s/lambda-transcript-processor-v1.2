import json
import os
import boto3
import uuid
import openai

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SessionTable')  # Replace with your DynamoDB table name

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.environ['OPENAPI_KEY']

def start_session_handler(transcript):
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    
    # Store the session data in DynamoDB
    table.put_item(Item={
        'SessionId': session_id,
        'Transcript': transcript,
        'Context': ''  # Placeholder for any initial context if needed
    })
    
    # Return the session ID to the client
    return {
        'statusCode': 200,
        'body': json.dumps({'sessionId': session_id, 'message': 'Session started'})
    }

def ask_question_handler(session_id, question):
    # Retrieve the session data from DynamoDB
    response = table.get_item(Key={'SessionId': session_id})
    if 'Item' in response:
        session_data = response['Item']
        transcript = session_data['Transcript']
        
        # Combine the transcript and the question to form the prompt
        prompt = f"{transcript}\n\n{question}"
        
        # Send the prompt to OpenAI's GPT-3.5-turbo model
        gpt_response = openai.Completion.create(
            engine="text-davinci-003",  # Replace with your chosen model
            prompt=prompt,
            max_tokens=1024  # Adjust as needed
        )
        
        # Extract the response text
        answer = gpt_response.choices[0].text.strip()
        
        # Return the answer to the client
        return {
            'statusCode': 200,
            'body': json.dumps({'answer': answer})
        }
    else:
        # Handle session not found
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Session not found'})
        }

def lambda_handler(event, context):
    path = event.get('rawPath', '')  # Get the path from the event object
    method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')
    
    if method == 'POST':
        body = json.loads(event.get('body', '{}'))
    
        if path == '/start-session' and 'transcript' in body:
            return start_session_handler(body['transcript'])
        
        elif path == '/ask-question' and 'sessionId' in body and 'question' in body:
            return ask_question_handler(body['sessionId'], body['question'])

    # Default response for invalid path or method
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Invalid path or method'})
    }
