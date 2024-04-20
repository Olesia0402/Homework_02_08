import json

from mongoengine.errors import NotUniqueError

from models import Author, Quote


def send_data_to_authors(author_file):
    with open (author_file, encoding='utf-8') as file:
        data = json.load(file)
        for el in data:
            try:
                author = Author(fullname = el.get('fullname'),
                                born_date = el.get('born_date'),
                                born_location = el.get('born_location'),
                                description = el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"Автор вже існує {el.get('fullname')}")

def send_data_to_quotes(quotes_file):
    with open(quotes_file, encoding='utf-8') as file:
        data = json.load(file)
        for el in data:
            author, *_ = Author.objects(fullname=el.get('author'))
            quote = Quote(tags = el.get('tags'),
                          author = author,
                          quote = el.get('quote'))
            quote.save()

if __name__ == '__main__':
    send_data_to_authors('authors.json')
    send_data_to_quotes('quotes.json')