from confluent_kafka import Producer
import random

p = Producer({
    'bootstrap.servers': 'localhost:9092'
})

for i in range(100):
    data = {'random_number:', random.randint(1,10)}
    p.produce('testtopic',str(data))
    
p.flush()