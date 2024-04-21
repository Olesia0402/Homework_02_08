import json
import pika
from bson.objectid import ObjectId
from faker import Faker
from mongoengine import connect
from mongoengine.errors import NotUniqueError

from models import User

fake_data = Faker()
count = 20

def create_contact():
    try:
        user = User(fullname=fake_data.name(),
                    email=fake_data.email(),
                    phone=fake_data.phone_number())
        user.save()
    except NotUniqueError:
        print(f"Користувач вже існує")

def generate_massege(user_id: str):
    message = {
            'id': user_id,
            'payload': f"Dear user, we are pleasure to say that you have a chanse to take part on the celebrationt birthday of our company."
        }
    return message

def save_contact_to_db(count:int):
    connect(db='database', host="mongodb+srv://olesyashevchuk0402:JeJ6Bb00zAnOUTRL@cluster0.ki8cwf1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    if count > 0:
        for i in range(count):
            create_contact()

def main(count:int):
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='email_exchange', exchange_type='direct')
    channel.queue_declare(queue='email_queue', durable=True)
    channel.queue_bind(exchange='email_exchange', queue='email_queue')
    
    users_id = [user.id for user in User.objects()]
    for user_id in users_id:
        message = generate_massege(str(user_id))

        channel.basic_publish(exchange='email_exchange', routing_key='email_queue', body=json.dumps(message).encode())

    connection.close()
    

if __name__ == '__main__':
    save_contact_to_db(count)
    main(count)