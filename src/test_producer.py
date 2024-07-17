from confluent_kafka import Producer


p = Producer({
    'bootstrap.servers': 'localhost:9092'
})

test_message = 'test message 2'
p.produce('py_test_topic',test_message)

p.flush() #forces the sending of the message from the buffer to the kafka cluster

