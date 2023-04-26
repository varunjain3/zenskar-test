## Deployment Instructions

---

1. Clone the repository

2. Start mysql server with docker-compose
```
$ cd mysql
$ mkdir data
$ docker-compose up -d
```
3. Create database and tables
```
$ mysql -h 127.0.0.1 -u admin -p
mysql> use admin;
mysql> CREATE TABLE customers (
        ID VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        HASH VARCHAR(255) NOT NULL,
        PRIMARY KEY (ID)
        );
```
4. Start kafka server with docker-compose
```
$ cd ../kafka
$ docker-compose up -d
```

5. create topic in kafka

```shell
$ docker-compose exec kafka kafka-topics --create --topic customers --partitions 1 --replication-factor 1 --if-not-exists --bootstrap-server 127.0.0.1:9092
```

6. Put Stripe API keys in environment variables

7. Run inward-sync as background service

8. Make a dummy change in system using make-dummy-queue.py

9. run outward-sync as background service to update stripe and database from the kafka queue


### Salesforce integration

based on the requirements, we can use the same kafka topics and add an event tag, to keep updating the stripe and database from the kafka queue based on saleforce api requirements.