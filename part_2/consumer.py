"""Rabbitmq consumer"""
from os import getenv
from typing import Any
import pickle

from pika import PlainCredentials, ConnectionParameters, BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel
from mongoengine import connect
from dotenv import load_dotenv

from models_odms import Contact

load_dotenv()
if ATLAS_HOST := getenv('ATLAS_HOST') is None:
    ATLAS_HOST = "mongodb://localhost/"
if ATLAS_PARAMS := getenv('ATLAS_PARAMS') is None:
    ATLAS_PARAMS = ""

DB_NAME = "pythonweb_hw08"

connect(host=ATLAS_HOST+DB_NAME+ATLAS_PARAMS)


def callback(channel: BlockingChannel,
             method: Any,
             properties: Any,
             body: Any):
    id_ = pickle.loads(body)
    contact = Contact.objects(id=id_).first()
    if contact.preferred == 'email':
        print(f"Email for {contact.name} is sent to {contact.email}")
    else:
        print(f"Sms for {contact.name} is sent to {contact.phone_number}")
    contact.is_sent = True
    contact.save()


def main():
    credentials = PlainCredentials(username='guest',
                                   password='guest')
    connection_params = ConnectionParameters(host='localhost',
                                             port=5672,
                                             credentials=credentials)
    connection = BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue='hw08_contacts_to_notify')

    channel.basic_consume(queue='hw08_contacts_to_notify',
                          on_message_callback=callback,
                          auto_ack=True)

    print("Waiting for messages. To exit press Ctrl-C.")
    channel.start_consuming()


if __name__ == "__main__":
    main()