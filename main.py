from flask import Flask, jsonify, abort, Response
import logging
import openai
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def generate_response(request):
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    try:
        request_data = request.get_json()

        if not request_data or 'message' not in request_data or 'history' not in request_data:
            return ('Bad Request: Missing fields', 400, headers)

        logger.info(f"Request {request}")

        logger.info(f"Request data {request_data}")

        message = request_data['message']
        history = request_data['history']


        system_message = [{"role": "system",
                           "content": f"""
Act as smart lawyer bot in the Republic of Kazakhstan. You name is ZangerAI. You can use the following information if needed ``` 1 Месячный расчетный показатель (МРП) на сегодняшний день равен 3450 тенге```. 
Don't make up facts. 
Important! Use the same language as used in user message ```{message}```.
If you cannot answer, then write that you cannot answer in the same language as user message"""}]
        messages = system_message + history + [{"role": "user", "content": message}]

        logger.info(f"Calling llm with {messages}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=1500
        )
        response_text = response.choices[0].message.content
        logger.info(f"Got the response {response_text}")
        return (json.dumps({"answer": response_text}), 200, headers)

    except Exception as e:
        return (str(e), 500, headers)


if __name__ == '__main__':
    app.run(debug=True)
