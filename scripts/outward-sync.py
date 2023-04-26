import stripe
import time
import hashlib
import json

from kafka import KafkaConsumer

from helper import hash_customer, check_database, stripe, connection, cursor, update_database

consumer = KafkaConsumer(
    'customers',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my_group',
    value_deserializer=lambda m: m.decode('utf-8')
)

# if any message is received, print the message
for message in consumer:
    print(f"Received message: {message.value}")

    message = json.loads(message.value)
    details = message['details']
    hash = hash_customer(details)

    id = details['id']
    result = check_database(id)

    if result is None:
        Exception("Error: User not found in database")
    if result[3] != hash:
        # customer details changed, update database, and stripe
        checkUpdate = update_database(
            details["id"], details["name"], details["email"], hash)
        if not checkUpdate:
            Exception("Error updating user to database")
        else:
            stripe.Customer.modify(
                id,
                name=details["name"],
                email=details["email"]
            )

