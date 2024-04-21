from mongoengine import connect, Document, StringField


connect(db='database', host="mongodb+srv://olesyashevchuk0402:JeJ6Bb00zAnOUTRL@cluster0.ki8cwf1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


class User(Document):
    fullname = StringField(required=True, unique=True)
    email = StringField()
    phone = StringField()
    flag = False
    meta = {"collection": "users"}