from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE


connect(db='database', host="mongodb+srv://olesyashevchuk0402:JeJ6Bb00zAnOUTRL@cluster0.ki8cwf1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=70)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField(max_length=30))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)