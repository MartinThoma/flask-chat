# Flask Chat App

This is a super simple chat app written with Flask and jQuery.

## Run it

Natively:

```
$ pip install -r requirements.txt
$ flask db upgrade
$ python wsgi.py
```

or with Docker:

```
docker image build -t chat:latest .
docker container run -d --publish 5000:5000 chat:latest
```


## What is missing?

This project is a learning exercise, so a couple of important things might
never come:

* User names / authentication
* Loading only parts of the complete chat log
* Editing of chat massages
* Search
