__author__ = 'mehdi'
import pika
import json


def send_verification_code(phone_number, verification_code):
    send_message = {"phone_number": phone_number,
                    "message": "کاربر گرامی کد فعال سازی بازی  o2 \n %s" % verification_code}
    message = json.dumps(send_message)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=message)
    print(" [x] Sent 'Hello World with python!'")
