from kafka import KafkaProducer
from helper import (
    stripe,
    create_message)
import json
import time


new_email = "Checking@gmail.com"
name = "Checking 3"
id = "cus_NmoTUEk9A4kcYA"


# Initialize Kafka producer with your Kafka broker address
producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

# from stripe call customer with id
customer = stripe.Customer.retrieve(id)

customer = dict(customer)
customer['email'] = new_email
customer['name'] = name

current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
customer_object = {
    "time": current_time,
    "details": customer
}

print(customer_object)

producer.send("customers", create_message(customer_object))

print("1 Message sent to Kafka Queue")
