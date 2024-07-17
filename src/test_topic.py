from confluent_kafka.admin import AdminClient,NewTopic

admin_client = AdminClient({
    'bootstrap.servers': 'localhost:9092'
})
                           
topic_name = 'py_test_topic'
partitions = 3
new_topic = NewTopic(topic_name, partitions)
result =admin_client.create_topics([new_topic])


# Print the result
for topic, future in result.items():
    try:
        future.result()
        print(f"Created the topic {topic_name}, with {partitions} partitions")
    except Exception as e:
        print(f"Failed to create the topic {topic_name}: {e}")

