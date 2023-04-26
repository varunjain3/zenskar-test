import time

from helper import (hash_customer,
                    update_database,
                    check_database,
                    add_to_database,
                    stripe)


def poll_for_updates():

    customers = stripe.Customer.list().data

    for customer in customers:

        result = check_database(customer.id)
        hash = hash_customer(dict(customer))

        if result is None:
            # add user to database
            checkUpdate = add_to_database(
                customer.id, customer.name, customer.email, hash)
            if not checkUpdate:
                Exception("Error adding user to database")

        elif result[3] != hash:
            # update user to database
            checkUpdate = update_database(
                customer.id, customer.name, customer.email, hash)
            if not checkUpdate:
                print()
                Exception("Error updating user to database")


if __name__ == "__main__":
    while True:
        poll_for_updates()
        time.sleep(10)
