# Other imports and initialization code remains the same

def delete_session_handler(session_id):
    # Delete the session data from DynamoDB
    response = table.delete_item(Key={'SessionId': session_id})
    
    # Return a success response to the client
    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Session {session_id} deleted successfully'})
    }

def lambda_handler(event, context):
    path = event.get('rawPath', '')  # Get the path from the event object
    method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')
    
    # Parsing the body in advance for POST requests
    if method == 'POST':
        body = json.loads(event.get('body', '{}'))
    
    if path == '/start-session' and method == 'POST' and 'transcript' in body:
        return start_session_handler(body['transcript'])
        
    elif path == '/ask-question' and method == 'POST' and 'sessionId' in body and 'question' in body:
        return ask_question_handler(body['sessionId'], body['question'])

    elif path == '/delete-session' and method == 'DELETE':
        # For a DELETE request, the session ID might come from query parameters or a JSON body
        session_id = event.get('queryStringParameters', {}).get('sessionId') or (json.loads(event.get('body', '{}')) if event.get('body') else {}).get('sessionId')
        if session_id:
            return delete_session_handler(session_id)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Session ID required for deletion'})
            }

    # Default response for invalid path or method
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Invalid path or method'})
    }
