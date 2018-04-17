Simple daily standup async bot for remote teams who use Slack.
--------
Made with `Django`, `AWS Lambda` and [zappa](https://github.com/Miserlou/Zappa) framework.

**You can now use Docker insted of Zappa**. Read below for instructions.

#### How it looks like?
Once a day a bot writes to selected members list of questions for standup.
Users and questions configured in Admin interface.

After user answer this questions the whole answer is posted to public channel.

![Standup demo](https://media.giphy.com/media/XIFHNMZv3Y4EreMsy7/giphy.gif)


#### How the result looks like?
Post in public channel

![Standup result](https://media.giphy.com/media/eBfokbeWeANx4GoQRk/giphy.gif)


## Prerequirements
In order to quickly use this bot you need to:
1. Create AWS account to use Lambda
2. Create new [Slack App](https://api.slack.com/apps) and Slack bot
3. Deploy a service with `zappa` and add a webhook for Slack bot
4. Tune bot with you texts and users
5. Authorize your app in you Slack team

Looks hard, but the whole process unlikely takes longer than 30 minutes.


## Settings file
All environment variables are stored into `slack/settings/settings.yml`
 file which is of course ignored. Because file is `yaml` we can create multiple environment
 and inherite them. So the file structure must be like that

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


  * `SECRET_KEY` — [Django secrete key](https://docs.djangoproject.com/en/2.0/ref/settings/). You can generate it [here](https://www.miniwebtool.com/django-secret-key-generator/).    
  * `DEBUG` — [Django debug key](https://docs.djangoproject.com/en/2.0/ref/settings/)
  * `DB_ENGINE`  — [Django engine for DB](https://docs.djangoproject.com/en/2.0/ref/settings/). We use Postgres with `django.db.backends.postgresql`.
  * `SLACK_CLIENT_ID` — Slack client id which you can find on your app page like `https://api.slack.com/apps/XXXXXX`
  * `SLACK_CLIENT_SECRET`  — Slack client secret which you can find on your app page like `https://api.slack.com/apps/XXXXXX`  
  * `SLACK_VERIFICATION_TOKEN` — Slack client verification token which you can find on your app page like `https://api.slack.com/apps/XXXXXX`
  * `SLACK_BOT_USER_TOKEN` —  Slack bot user token which you can find on your app page in `bot users` section
  * `TEXT_NO_MORE_QUESTIONS` —  The text when user has submitted standut for today and writes another message 
  * `TEXT_STANDUP_IS_DONE` —  A greeting message which is sent right after the answer for the last question
  * `TEXT_NO_USER` —  A message for user which shouldn't write standup (for example, if somebody randomly sent a message to a bot)
  * `TEXT_CHANNEL_MESSAGE` —  A message template for user for a public channel. Users mention is inside. For example ```'<@{}> закончил стэндап. Красава!'```
  * `TEXT_NEW_DAY` —  A welcome message for a new day standup
  * `SLACK_COMMON_CHANNEL` —  Channel ID for public standup. Can be easily found when open a channel. Take a look at the url `https://teamname.slack.com/messages/*CHANNEL_ID*/details/`.


## Deploy
Be sure you have `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` environment variables set.

#### Zappa
To deploy a bot with Zappa just write `zappa deploy dev`. Zappa will create CloudFormation stack
for you to manage all the infrastructure. When you need yo update you stack write `zappa update dev`.

#### Docker
You need to build Docker image with command `docker build -t your_tag_name .`. Then run container with command `docker run -p 3720:3720 your_tag_name` where 3720 is a default port in Docker file. You can change the port for any other. In order to use CRON to start standup, you need some trigger. The easiest solution is to make a simple Lambda function that will trigger bot's API. Take a look at `scheduler.py` file. You can use alternative schedulers but for Lambda you need to
1. Create a file `local.yml` with content
```
dev:
  SCHEDULER_URL: your_url
```
where `dev` is a name of the environment, `SCHEDULER_URL` is a URL that sends standup to all users. For current settings, it would look like `your_domain:3720/send_standup`.

2. Tune CRON settings in `serverless.yml` file.
3. Deploy Lambda with [Serverless framework](https://serverless.com/) `sls deploy`.


## Zappa settings
You can tune deploy settings in `zappa_settings.json` file.

For example, you might want to change you standup start day (our when standup is sent). 


## Admin interface
The admin interface is available with Django interface. When you've deployed a service with
Zappa admin interface will be available by `/admin` url (without static files). Don't
forget to create superuser (`python manager.py createsuperuser --settings=slack.settings.dev`).
Add questions with the order.

You also need to add user for standup. For example, in our team only developers write standups.
Just fill `Slack id` for user and mark `Is active`. You can find `Slack id` in the url when 
open users profile. For example, `https://team.slack.com/messages/channel_id/team/USER_ID/`.
You don't need to fill `Channel id` for user.
