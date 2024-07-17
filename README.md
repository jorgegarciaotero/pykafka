# KAFKA

#### Levantar entorno
docker-compose up -d
docker exec -u root -it kafka-1 /bin/bash
docker cp src/test.py kafka-1:/confluence/src/

#### Kafka config dir:
cd /opt/bitnami/kafka/config/server.properties
- Log retention: 
  - log.retention.hours = 168
  - log.retention.bytes = 123123
- Partitions:
  - num.partitions = 2 #default number of partition when a topic is created.
 
#### Kafka TOPICS: kafka-topics.sh 
docker exec -it kafka-1 /bin/bash

- Una vez dentro del contenedor, puedes usar las herramientas de Kafka. Por ejemplo, para crear un nuevo topic:
kafka-topics.sh --create --topic my-topic-2 --bootstrap-server localhost:9092 --partitions 2 --replication-factor 2

- Para listar los topics:
kafka-topics.sh --list --bootstrap-server localhost:9092

- Para enviar mensajes a un topic:
kafka-console-producer.sh --topic my-topic --bootstrap-server localhost:9092

- Para consumir mensajes de un topic:
kafka-console-consumer.sh --topic my-topic --from-beginning --bootstrap-server localhost:9092

- Para comprobar la descripción del topic creado:
  kafka-topics.sh --bootstrap-server localhost:9092 --topic my-topic --describe

- Para borrar un topic:
kafka-topics.sh --bootstrap-server localhost:9092 --topic my-topic --delete


#### Kafka PRODUCER: kafka-console-producer.sh
- Enviar mensajes a un topic pruebaparticiones. El topic tiene 2 particiones por lo que los mensajes se almacenarán aleatoriamente en una partición o en otra.
  ```kafka-console-producer.sh --bootstrap-server localhost:9092 --topic pruebaparticiones```

- Enviar mensajes a un topic pruebaparticiones, especificando la partición. Para ello se usan las claves. 
    ```kafka-console-producer.sh --bootstrap-server localhost:9092 --topic pruebaparticiones  --property parse.key=true --property key.separator=:```

    El separador entre clave y valor son ":". Así los mensajes que le envío deben ser tal que "clave:valor". Ejemplo:
    ```bash
    kafka-console-producer.sh --bootstrap-server localhost:9092 --topic pruebaparticiones --property parse.key=true --property key.separator=:
    >clave:valor
    >pais:peru
    >pais:uruguay
    >pais:españa
    >pais:colombia
    ```

    Todo lo que lleve la misma clave, irá a la misma partición.

- Enviar mensajes y recibir confirmación de que el consumer ha recibido el mensaje:
    ```kafka-console-producer.sh --bootstrap-server localhost:9092 --topic pruebaparticiones  --producer-property acks=all```


#### Kafka CONSUMER: kafka-console-consumer.sh 
- Suscribirme a un topic para recibir mensajes: 
    ```kafka-console-consumer.sh --topic pruebaparticiones --from-beginning --bootstrap-server localhost:9092```
- Recibir toda la info desde el inicio:
    ```kafka-console-consumer.sh --topic pruebaparticiones --from-beginning --bootstrap-server localhost:9092 --from-beginning```
- Recibir mensajes de particiones, fecha de creacion, etc. impresas por pantalla.
    ```kafka-console-consumer.sh --topic pruebaparticiones --from-beginning --bootstrap-server localhost:9092 --formatter kafka.tools.DefaultMessageFormatter --property print.timestamp=true --property print.key=true --property print.value=true --property print.partition=true```
- Asociar un consumidor a un grupo de consumidores 
  - Creo topic: 
    ```kafka-topics.sh --create --topic mytopic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1```
  - Creo producer:
    ```kafka-console-producer.sh --bootstrap-server localhost:9092 --topic topicgroup --producer-property partitioner.class=org.apache.kafka.clients.producer.RoundRobinPartitioner```   
  - Creo consumers: 
    ```kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic mytopic --group myconsumergroup```
    ```kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic mytopic --group myconsumergroup```
    ```kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic mytopic --group myconsumergroup```
 - Información sobre el grupo de consumidores myconsumergroup:
    ```kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group myconsumergroup```

    GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID                                           HOST            CLIENT-ID
    myconsumergroup mytopic         0          2               2               0               console-consumer-6eb490e8-6d43-4405-85af-3e275acf2fbb /127.0.0.1      console-consumer
    myconsumergroup mytopic         1          1               1               0               console-consumer-6eb490e8-6d43-4405-85af-3e275acf2fbb /127.0.0.1      console-consumer
    myconsumergroup mytopic         2          2               2               0               console-consumer-943479fe-593b-4232-98bd-2c4e43914197 /127.0.0.1      console-consumer 

    - Group: Nombre del grupo de consumidores, en este caso myconsumergroup.
    - Topic: Nimbre del topic que los consumidores están consumiendo.
    - Partition: Nº de la partición del topic que se está consumiendo. Tenemos 3 particiones.
    - Current-offset: La posición actual del consumidor en la partición, el último offset que el consumidor ha procesado.
    - Log-end-offset: Último mensaje en la partición. Es el offset del mensaje más reciente en el log.
    - Lag: diferencia entre LOG-END-OFFSET y CURRENT-OFFSET. Indica cuántos mensajes más tiene que procesar el consumidor. Un lag de 0 significa que el consumidor está al día con la cola. 
    - CONSUMER-ID: El ID del consumidor que está procesando la partición. Es un identificador único para cada instancia del consumidor.
    - HOST: La dirección del host donde se está ejecutando el consumidor.
    - CLIENT-ID: El ID del cliente Kafka. Este es el identificador del cliente utilizado por el consumidor.


# PyKAFKA
#### Confluent doc: 
https://docs.confluent.io/platform/current/overview.html
https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html
