from confluent_kafka import Consumer
import pandas as pd
from io import StringIO



topic_name='testtopic'
consumer_group = 'test_group'

c=Consumer({
    'bootstrap.servers':'localhost:9092',
    'group.id':consumer_group,
    'auto.offset.reset':'earliest'
})
c.subscribe([topic_name])

dataframe=pd.DataFrame(columns=['Column_1','Column_2','Column_3','Column_4','Column_5'])

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            print("No message, keep listening")
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue
        else:
            print(f"Message Value: {msg.value().decode('utf-8')}")
            print(f"Message Key: {msg.key()}")
            print(f"Message Topic: {msg.topic()}")
            print(f"Message Partition: {msg.partition()}")
            print(f"Message Offset: {msg.offset()}")
            message_data = StringIO(msg.value().decode('utf-8'))
            row_data = pd.read_csv(message_data,
                                    header=None,
                                    names=['Column_1','Column_2','Column_3','Column_4','Column_5']
                                    )
            dataframe =pd.concat([dataframe,row_data],ignore_index=True)
            print("llega?")
            print("dataframe: \n",dataframe)
            print("")
            
except KeyboardInterrupt:
    pass
finally:
    c.close()
    print("DATAFRAME FINAL: \n",dataframe)
