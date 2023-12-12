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

def lambda_handler(event, context):
    # Extract the transcript and question from the request
    transcript = event.get('transcript')
    question = event.get('question')
    
    # If a transcript is provided, start the session and get the session ID
    if transcript:
        session_id = start_session(transcript)
        # If a question is provided along with the transcript, get an answer
        if question:
            answer = ask_question(transcript, question)
            return {
                'statusCode': 200,
                'body': json.dumps({'sessionId': session_id, 'answer': answer})
            }
        else:
            # If no question is provided, just return the session ID
            return {
                'statusCode': 200,
                'body': json.dumps({'sessionId': session_id})
            }
    # If only a question is provided, fetch the transcript from the session and return an answer
    elif question and 'sessionId' in event:
        session_id = event['sessionId']
        # Retrieve the session data from DynamoDB
        response = table.get_item(Key={'SessionId': session_id})
        if 'Item' in response:
            session_data = response['Item']
            answer = ask_question(session_data['Transcript'], question)
            return {
                'statusCode': 200,
                'body': json.dumps({'answer': answer})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Session not found'})
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No transcript or question provided'})
        }
