#!/usr/bin/env python3
import argparse
import json
import pika
import sys

def set_parser():
	parser = argparse.ArgumentParser()

	parser.add_argument("--app", help="App Name", required=True)
	parser.add_argument("--device", help="Device Name", required=True)

	return parser


if __name__== "__main__":
	parser = set_parser()
	args = parser.parse_args()

	# if args.app or args.device:
	#	 raise ValueError()

	connection = pika.BlockingConnection(pika.ConnectionParameters('172.18.0.2'))
	channel = connection.channel()

	channel.queue_declare(queue='u2f_sign_queue', durable=True)
	message = json.dumps(vars(args))
	channel.basic_publish(exchange='',
						routing_key='u2f_sign_queue',
						body=message,
						properties=pika.BasicProperties(delivery_mode = pika.DeliveryMode.Persistent))
	print(f"Message: {message}: sent succesfully!")

	connection.close()