from typing import List, Any
from mongoengine import connect

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)
connect(db='database', host="mongodb+srv://olesyashevchuk0402:JeJ6Bb00zAnOUTRL@cluster0.ki8cwf1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

@cache
def find_by_tag(tag:str) -> list:
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result

@cache
def find_by_author(author:str) -> list:
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result

def find_by_tags(tags: list) -> list:
    quotes = Quote.objects(tags__all=tags)
    result = [q.quote for q in quotes]
    return result

def main():
    while True:
        command = input('Enter your search data: ')
        if command == 'exit':
            break
        else:
            func_word, search_word = command.split(':')
            if func_word == 'name':
                result = find_by_author(search_word)
            elif func_word == 'tag':
                result = find_by_tag(search_word)
            elif func_word == 'tags':
                tags = search_word.split(',')
                result = find_by_tags(tags)
            else:
                continue
            print(result)


if __name__ == '__main__':
    main()


