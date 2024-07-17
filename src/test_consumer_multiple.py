from confluent_kafka import Consumer,TopicPartition


topic_name='py_test_topic'
consumer_group = 'test_group'
partition_id=2

c=Consumer({
    'bootstrap.servers':'localhost:9092',
    'group.id':consumer_group,
    'auto.offset.reset':'earliest'
})
#c.subscribe([topic_name])
c.assign([TopicPartition(topic_name,partition_id)])

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            print("No message, keep listning")
            continue
        print(f"Message Value: {msg.value().decode('utf-8')}")
        print(f"Message Key: {msg.key()}")
        print(f"Message Topic: {msg.topic()}")
        print(f"Message Partition: {msg.partition()}")
        print(f"Message Offset: {msg.offset()}")
except KeyboardInterrupt:
    pass
finally:
    c.close()