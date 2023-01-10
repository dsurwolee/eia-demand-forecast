from kafka import KafkaConsumer

TOPIC_NAME = 'items'

consumer = KafkaConsumer(TOPIC_NAME)
for message in consumer:
	print(message)

# https://www.youtube.com/watch?v=qbROwuuDOJA
#  https://hevodata.com/learn/kafka-python/