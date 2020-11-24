import os
from google.cloud import pubsub_v1
import uuid
import logger_tests
from inspect import getmembers, isfunction


_test_functions = {name:func for (name,func) in getmembers(logger_tests) 
                             if isfunction(func)}

def callback(message):
    msg_str = message.data.decode('utf-8')
    message.ack()
    found_func = _test_functions.get(msg_str, None)
    if found_func:
        found_func()
    else:
        print(f'function {msg_str} not found')

if __name__ == "__main__":
    # set up pubsub listener
    topic_id = 'logging-test'
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT')
    subscription_id = f"logging-{uuid.uuid4().hex}"


    subscriber = pubsub_v1.SubscriberClient()
    topic_name = f'projects/{project_id}/topics/{topic_id}'
    subscription_name = f'projects/{project_id}/subscriptions/{subscription_id}'
    subscriber.create_subscription(name=subscription_name, topic=topic_name)
    future = subscriber.subscribe(subscription_name, callback)
    try:
        print('listening for pubsub messages')
        future.result()
    except KeyboardInterrupt:
        future.cancel()
