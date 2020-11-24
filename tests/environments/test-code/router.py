import os
from google.cloud import pubsub_v1
import uuid
import logger_tests
from inspect import getmembers, isfunction
import google.cloud.logging
import google.auth
import logging
from flask import Flask, request
import base64

app = Flask(__name__)

_test_functions = {name:func for (name,func) in getmembers(logger_tests) 
                             if isfunction(func)}

# grabs pubsub message out of request
# used in Cloud Run
@app.route('/', methods=['POST'])
def pubsub_http():
    envelope = request.get_json()
    if not envelope or not isinstance(envelope, dict) or 'message' not in envelope:
        return f'Bad Request: invalid pub/sub message', 400
    pubsub_message = envelope['message']
    msg_str = base64.b64decode(pubsub_message['data']).decode('utf-8').strip()
    found_func = _test_functions.get(msg_str, None)
    if found_func:
        found_func()
        return ('', 200)
    else:
        return f'Bad Request: function {msg_str} not found', 400

# recieves pubsub messages when the script is run directly (GKE)
def pubsub_callback(message):
    msg_str = message.data.decode('utf-8')
    message.ack()
    found_func = _test_functions.get(msg_str, None)
    if found_func:
        found_func()
    else:
        print(f'function {msg_str} not found')


if __name__ == "__main__":
    # set up logging
    client = google.cloud.logging.Client()
    client.setup_logging()

    if os.getenv('ENABLE_SUBSCRIBER', None):
        # set up pubsub listener
        topic_id = 'logging-test'
        _, project_id = google.auth.default()
        subscription_id = f"logging-{uuid.uuid4().hex}"
        subscriber = pubsub_v1.SubscriberClient()
        topic_name = f'projects/{project_id}/topics/{topic_id}'
        subscription_name = f'projects/{project_id}/subscriptions/{subscription_id}'
        subscriber.create_subscription(name=subscription_name, topic=topic_name)
        future = subscriber.subscribe(subscription_name, pubsub_callback)
        try:
            print('listening for pubsub messages')
            future.result()
        except KeyboardInterrupt:
            future.cancel()

    # set up flask server
    if os.getenv('ENABLE_FLASK', None):
        port = os.getenv('PORT', 8080)
        app.run(debug=True, host='0.0.0.0', port=port)
