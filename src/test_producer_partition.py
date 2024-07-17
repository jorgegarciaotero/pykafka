from confluent_kafka import Producer


p = Producer({
    'bootstrap.servers': 'localhost:9092'
})

topic_name = 'py_test_topic'
partition_id = 2#partition 1 of py_test_topic
test_message = 'test message 4'

p.produce(topic=topic_name,value=test_message, partition=partition_id)

p.flush() #forces the sending of the message from the buffer to the kafka cluster

