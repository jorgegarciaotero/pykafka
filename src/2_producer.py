from confluent_kafka import Producer
import random
import pandas as pd

p = Producer({
    'bootstrap.servers': 'localhost:9092'
})

dataframe = pd.read_csv('file.csv')
print(f"dataframe: {dataframe}")
print(f"dataframe.columns: {dataframe.columns}")


for _,row in dataframe.iterrows():
    
    print(f"row: {row}")
    message = f"{row['Column_1']},{row['Column_2']}, {row['Column_3']}, {row['Column_4']}, {row['Column_5']}"
    print(f"message: {message}")
    p.produce('testtopic',value=message)
    
p.flush()