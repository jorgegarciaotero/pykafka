from confluent_kafka import Producer
import requests
import json
import time
import yaml
import sys
import os
import logger as lg
import traceback
 
def producer_configuration(config,logger):
    '''
    Config and return a Kafka producer Object.
    Args:
    - config: dict that contains Producer config from  config.yaml.
    - logger: logger object to register events.
    Returns:
    - Producer: Producer's object
    '''
    producer = None
    try:
        logger.info("Building the producer.")
        producer_conf = config['producer_conf']
        producer = Producer(producer_conf)
        logger.info("Producer Built.")
        return producer
    except Exception as e:
        logger.error("Error in the producer construction: %s", e, exc_info=True)
        return None
        


def request_data(producer,config,logger):
    '''
    Load the API's URL from the config .yaml, requests the data and serves it.
    Args: 
        - produce: producer's object
        - config: config's file
        - logger: logger object to register events.
    Returns:
        - None
    '''
    try:
        cryptos_to_track = config['cryptos_to_track']
        topic_name = config['topic_name']
        api_url = config['api_url']
        while True:
            response = requests.get(api_url)
            sleep_time = 30
            if response.status_code == 200:
                data = response.json()
                logger.info(f"data: {data}")
                if 'data' in data and isinstance(data['data'],list):
                    rows = [{'timestamp': int(time.time()),'name':crypto['name'],'price':crypto['priceUsd'],'symbol':crypto['symbol']} for crypto in data['data'] if crypto['id'] in cryptos_to_track]
                    for row in rows:
                        producer.produce(topic_name,value=json.dumps(row))
                    producer.flush()
                    logger.info("data sent to kafka")
            else:
                logger.error(f"Error in response. Status of the response is: {response.status_code}")
            time.sleep(sleep_time)
    except Exception as e:
        logger.error("Error in the producer construction: %s", e, exc_info=True)
        return None
        

def main():
    '''
    Producer's process for extracting cripto currencies from Coincap's API
    ''' 
    with open('config.yaml','r') as file:
        config = yaml.safe_load(file)
    producer_logger_path = config['producer_logger_path']
    logger = lg.setup_logger('producer', producer_logger_path)
    logger.info('Starting Producer Process.')
    producer=producer_configuration(config,logger)   
    logger.info("Requesting data from the API")
    request_data(producer,config,logger)
    logger.info("Process Finished")

if __name__=="__main__":
    main()