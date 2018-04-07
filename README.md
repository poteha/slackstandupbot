Simple daily standup async bot for remote teams who use Slack.
--------
Made with `Django`, `AWS Lambda` and [zappa](https://github.com/Miserlou/Zappa) framework.

#### How it looks like?

![Standup demo](https://media.giphy.com/media/XIFHNMZv3Y4EreMsy7/giphy.gif)


#### How the result looks like?

![Standup result](https://media.giphy.com/media/eBfokbeWeANx4GoQRk/giphy.gif)


## Prerequirements
In order to quickly use this bot you need to:
1. Create AWS account to use Lambda
2. Create new [Slack App](https://api.slack.com/apps) and Slack bot
3. Deploy a service with `zappa` and add a webhook for Slack bot
4. Tune bot with you texts and users
5. Authorize your app in you Slack team

Looks hard, but the whole process unlikely takes longer than 30 minutes.


## Quick deploy


## Settings file



```
default_env: &default_env
  SECRET_KEY: 
  DEBUG: true
  DB_ENGINE: 'django.db.backends.postgresql'
  SLACK_CLIENT_ID: 
  SLACK_CLIENT_SECRET: 
  SLACK_VERIFICATION_TOKEN: 
  SLACK_BOT_USER_TOKEN: 
  TEXT_NO_MORE_QUESTIONS: 'Красава, ты уже отправил сегодняшний стэндап.'
  TEXT_STANDUP_IS_DONE: 'Стэндап закончен :tada:. Спасибо за ответы!'
  TEXT_NO_USER: 'Тебе проходить стэндап не нужно.'
  TEXT_CHANNEL_MESSAGE: '<@{}> закончил стэндап. Красава!'
  TEXT_NEW_DAY: 'Привет! Пришло время нового стэндапа.'
  SLACK_COMMON_CHANNEL: 
```

```
local:
  <<: *default_env
  SECRET_KEY: 
  DB_NAME: 
  DB_HOST: 
  DB_PORT: 
  DB_USER: 
  DB_PASSWORD: 
```

```
dev:
  <<: *default_env
  SECRET_KEY: 
  DEBUG: false
  DB_NAME: 
  DB_HOST: 
  DB_PORT: 
  DB_USER: 
  DB_PASSWORD: 
```

## Deploy
`zappa deploy dev`

`zappa update dev`
