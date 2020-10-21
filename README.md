# Notekeeper - Slack bot for keeping notes
This project is django-based application that runs web-server
and accepts slack webhooks when bot name is mentioned in message
See https://api.slack.com/legacy/custom-integrations/outgoing-webhooks#legacy-info
on how to configure outgoing webhooks in Slack

## Requirements 
Project uses `python 3.8` and `poetry` as dependency manager.
To use it fom slack, you need to install and configure [slack app](https://fan-tomworkspace.slack.com/apps/A0F7VRG6Q-outgoing-webhook)

## Setup

- clone the repo
```
$ git clone https://github.com/fan-tom/notekeeper
$ cd notekeeper
```

- install dependencies

`$ poetry install`

- apply default settings

`$ cp .env.example .env`

- run database

`$ doker-compose up -d`

- run migrations

`$ ./manage.py migrate`

- run tests

```
$ cd slack
$ ./manage.py test tests/
```

- run server

`$ ./manage.py runserver`

App is run on `8000` port

Now configure hook url in slack (it must end with `/slackhook/`, i.e `http://mydomain.com/slackhook/`)
and add `SLACK_TOKEN` to your environment variables (or .env), with value from app configuration page
If you don't have domain name, you may use `ngrok` to get it (temporary and ugly)

## Slack API
Now you can write `nnotekeeper help` in slack message and get help for bot.
Bot accepts two commands: `push <text>` and `top [<n>]`.
Push command adds `text` to notes list.
Top command can show `n` last notes (1 if `n` is not specified)

## Admin API
Also there are two endpoints to get some statistics about notes

- `/notekeeper/stats/notes-number/[user_id]`

    get number of notes, optionally filtered by user id and datetime range (from_date/to_date query parameters, ISO-8601)

    example:

    `curl http://localhost:8000/notekeeper/stats/top-used-words?n=2&from_date=2019-01-01T02:03:04.5&to_date=2020-11-05T19:54:08.45`

- `/notekeeper/stats/top-used-words`

    get top used words (`n` query parameter, 1 if omitted), optionally filtered by datetime range (from_date/to_date query parameters, ISO-8601)

    example:

    `curl http://localhost:8000/notekeeper/stats/notes-number/U12345?from_date=2019-01-01T02:03:04.5&to_date=2020-11-05T19:54:08.45`
