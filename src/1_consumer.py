from confluent_kafka import Consumer
import pandas as pd


topic_name='testtopic'
consumer_group = 'test_group'

c=Consumer({
    'bootstrap.servers':'localhost:9092',
    'group.id':consumer_group,
    'auto.offset.reset':'earliest'
})
c.subscribe([topic_name])

data_consumer=[]

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            print("No message, keep listening")
            continue
        print(f"Message Value: {msg.value().decode('utf-8')}")
        print(f"Message Key: {msg.key()}")
        print(f"Message Topic: {msg.topic()}")
        print(f"Message Partition: {msg.partition()}")
        print(f"Message Offset: {msg.offset()}")
        data_consumer.append(msg.value().decode('utf-8'))
        print(f"data_consumer: {data_consumer}")
except KeyboardInterrupt:
    pass
finally:
    c.close()
    dataframe=pd.DataFrame(data_consumer)     
    print("DATAFRAME: \n",dataframe)
