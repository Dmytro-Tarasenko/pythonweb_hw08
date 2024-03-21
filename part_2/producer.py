"""Producer for rabbitmq"""
from os import getenv
from random import choice
import pickle

from mongoengine import connect
from dotenv import load_dotenv
from pika import PlainCredentials, BlockingConnection, ConnectionParameters
from faker import Faker

from models_odms import Contact

load_dotenv()
if ATLAS_HOST := getenv('ATLAS_HOST') is None:
    ATLAS_HOST = "mongodb://localhost/"
if ATLAS_PARAMS := getenv('ATLAS_PARAMS') is None:
    ATLAS_PARAMS = ""

DB_NAME = "pythonweb_hw08"

connect(host=ATLAS_HOST+DB_NAME+ATLAS_PARAMS)

def seed_db(count: int = 10) -> None:
    fake = Faker()

    for _ in range(count):
        name = fake.name()
        phone_number = fake.phone_number()
        email = fake.email()
        preferred = choice(['email', 'sms'])
        contact = Contact(name=name,
                          phone_number=phone_number,
                          email=email,
                          preferred=preferred)
        contact.save()



def main() -> None:
    credentials = PlainCredentials(username='guest',
                                   password='guest')
    connection_params = ConnectionParameters(host='localhost',
                                             port=5672,
                                             credentials=credentials)
    connection = BlockingConnection(connection_params)

    channel = connection.channel()
    main_queue = channel.queue_declare(queue='hw08_contacts_to_notify')
    for contact in Contact.objects().all():
        if not contact.is_sent:
            id_ = contact.id
            print(id_)
            channel.basic_publish(exchange='',
                                  routing_key='hw08_contacts_to_notify',
                                  body=pickle.dumps(id_))
    connection.close()

if __name__ == "__main__":
    # seed_db(count=25)
    main()
