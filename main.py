from confluent_kafka import Consumer

# IBM Event Streams parameters
topic = "activity-tracker"
bootstrap_servers = ''
api_key = ''

conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'mygroup',
        'session.timeout.ms': 6000,
        'auto.offset.reset': 'earliest',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': 'token',
        'sasl.password': api_key
        }

print("Creating consumer");
c = Consumer(
  {
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

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()
