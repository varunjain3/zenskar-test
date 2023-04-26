import stripe
import hashlib
import json
import os

from mysql.connector import connect, Error

# Initialize Stripe API with your secret key
stripe.api_key = os.environ.get("STRIPE_API_KEY")

# hashing function
dhash = hashlib.md5()

# Connect to your MySQL database
try:
    connection = connect(
        host="localhost",
        user="admin",
        password="admin",
        database="admin"
    )
    cursor = connection.cursor()
except Error as e:
    print(e)

# to hash customer information for quick comparison


def hash_customer(customer_details):
    # details = f"{customer_details["name"]}{customer_details["email"]}{customer_details["id"]}" 
    check = {
        "name": customer_details["name"],
        "email": customer_details["email"],
        "id": customer_details["id"]
    }
    encoded = json.dumps(check, sort_keys=True).encode()
    return hashlib.md5(encoded).hexdigest()


def add_to_database(id, name, email, hash):
    try:
        query = "INSERT INTO customers (ID, name, email, HASH) VALUES (%s, %s, %s, %s)"
        values = (id, name, email, hash)
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(e)
        return False


def update_database(id, name, email, hash):
    try:
        query = "UPDATE customers SET name = %s, email = %s, HASH = %s WHERE ID = %s"
        values = (name, email, hash, id)
        cursor.execute(query, values)
        connection.commit()
        return True
    except Error as e:
        print(e)
        return False


def check_database(id):
    query = "SELECT * FROM customers WHERE ID = %s"
    values = (id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    return result


def create_message(message: dict):
    message = json.dumps(message)
    return message.encode("utf-8")
