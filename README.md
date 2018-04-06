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