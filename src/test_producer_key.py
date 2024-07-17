from confluent_kafka import Producer

print("start")

p = Producer({
    'bootstrap.servers': 'localhost:9092'
})

topic_name = 'py_test_topic'
key = 'country'
value = 'england'

p.produce(topic=topic_name, key=key,value=value)

p.flush() #forces the sending of the message from the buffer to the kafka cluster

print("END")