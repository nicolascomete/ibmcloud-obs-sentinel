from confluent_kafka import Consumer
import os
import requests
import datetime
import hashlib
import hmac
import base64
import json


# IBM Cloud Event Streams env vars
bootstrap_servers = os.environ['EVENT_STREAMS_BOOTSTRAP_SERVERS']
api_key = os.environ['EVENT_STREAMS_API_KEY']
topic = "activity-tracker"

# MS Sentinel env vars
customer_id = os.environ['MS_SENTINEL_WORKSPACE_ID']
shared_key = os.environ['MS_SENTINEL_AUTH_KEY']
sentinel_log_type = <CHANGEME>

# Build the API signature for Sentinel
def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
    x_headers = 'x-ms-date:' + date
    string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
    bytes_to_hash = bytes(string_to_hash, encoding="utf-8")
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
    authorization = "SharedKey {}:{}".format(customer_id,encoded_hash)
    return authorization

# Build and send a request to the POST API
def post_data(customer_id, shared_key, body, log_type):
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)
    uri = 'https://' + customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }

    response = requests.post(uri,data=body, headers=headers)
    if (response.status_code >= 200 and response.status_code <= 299):
        print('Message successfully sent to Sentinel')
    else:
        print(f"Unable to send message to Sentinel (status code ={response.status_code})")


# Callback for message received on topic
def received_message(msg):
    print("\nReceived new message on Event Streams")

    # Check if this is a test message
    if msg.startswith('LogDNA test message:'):
        print(f'Received test message: "{msg}"')
        return

    try:
        print("Trying to convert message to JSON")
        json_msg = json.loads(msg)
        print("Posting JSON to Sentinel")
        post_data(customer_id, shared_key, json.dumps(json_msg), sentinel_log_type)
    except JSONDecodeError:
        print('Warning: discarding malformed JSON message (see below)')
        print(msg)
        

# Main flow (poll Event Streams for new messages)
# -----------------------------------------------

print("Creating consumer");
c = Consumer({
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'mygroup',
    'session.timeout.ms': 6000,
    'auto.offset.reset': 'earliest',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': 'token',
    'sasl.password': api_key
  }
)

print(f"Subscribing to topic '{topic}'")
c.subscribe([topic])

print("Waiting on messages...")
while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue
   
    received_message(msg.value().decode('utf-8'))

c.close()
