from confluent_kafka import Consumer
import csv
import json
import time
import yaml
import sys
import os
import logger as lg
import traceback



def consumer_configuration(config,logger):
    '''
    Configs and returns a Kafka Consumer Object.
    Args:
    - config: dict that contains Consumer's config from  config.yaml.
    - logger: logger object to register events.
    Returns:
    - Consumer: Consumers's object
    '''
    consumer = None
    try:
        logger.info("Creating the Consumer.")
        consumer_conf = config['consumer_conf']
        topic_name = config['topic_name']
        consumer = Consumer(consumer_conf)
        consumer.subscribe([topic_name])
        logger.info("Consumer Created.")
        return consumer
    except Exception as e:
        logger.error("Error in the consumer construction: %s", e, exc_info=True)
        return None


def consume_data(consumer,logger):
    '''
    Consume the Kafka messages and write into csv
    Args: 
        - consumer: consumer's object
        - logger: logger object to register events.
    Returns:
        - None
    '''
    try:
        logger.info("Creating the CSV file")
        csv_file_path = 'crypto_prices.csv'
        logger.info("Writing data into the CSV file")
        with open(csv_file_path,'a',newline='') as csv_file:
            writer = csv.DictWriter(csv_file,fieldnames=['timestamp','name','price','symbol'])
            #Write header if the file does not exist
            if not csv_file.tell():
                writer.writeheader()
            #Consume the Kafka messages and write into csv
            try:
                while True:
                    msg = consumer.poll(1.0)
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
                    row = json.loads(msg.value().decode('utf-8'))
                    writer.writerow(row)
                    print(f"data recibed and stored in {csv_file_path}")
            except KeyboardInterrupt:
                pass
            finally:
                consumer.close()
                print("Consumer closed. Final data written in the CSV file")
                time.sleep(2)
    except Exception as e:
        logger.error("Error in saving the data: %s", e, exc_info=True)
        return None
            

def main():
    '''
    Consumer's process for extracting cripto currencies from Coincap's API
    ''' 
    with open('config.yaml','r') as file:
        config = yaml.safe_load(file)
    consumer_logger_path = config['consumer_logger_path']
    logger = lg.setup_logger('consumer', consumer_logger_path)
    logger.info('Starting Consumer Process.')
    consumer=consumer_configuration(config,logger)   
    logger.info("Requesting data from  the API")
    consume_data(consumer,logger)
    logger.info("Process Finished")



if __name__=="__main__":
    main()