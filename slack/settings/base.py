import os
import yaml
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'standupbot'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'slack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'slack.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


#### TO OVERLOAD
SETTINGS_PATH = './slack/settings/settings.yml'
ENVIRONMENT = os.environ.get("ENVIRONMENT", 'local')
with open(SETTINGS_PATH) as f:
    configs = yaml.load(f)[ENVIRONMENT]


def get_env_var(setting, configs=configs):
    try:
        val = configs[setting]
        if val == 'True':
            val = True
        elif val == 'False':
            val = False
        return val
    except KeyError:
        error_msg = "ImproperlyConfigured: Set {0} environment      variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = configs['SECRET_KEY']
DEBUG = configs['DEBUG']


DATABASES = {
    'default': {
        'ENGINE': configs['DB_ENGINE'],
        'NAME': configs['DB_NAME'],
        'HOST': configs['DB_HOST'],
        'PORT': configs['DB_PORT'],
        'USER': configs['DB_USER'],
        'PASSWORD': configs['DB_PASSWORD']
    }
}

STATIC_URL = '/static/'

SLACK_CLIENT_ID = configs['SLACK_CLIENT_ID']
SLACK_CLIENT_SECRET = configs['SLACK_CLIENT_SECRET']
SLACK_VERIFICATION_TOKEN = configs['SLACK_VERIFICATION_TOKEN']
SLACK_BOT_USER_TOKEN = configs['SLACK_BOT_USER_TOKEN']

TEXT_NO_MORE_QUESTIONS = configs['TEXT_NO_MORE_QUESTIONS']
TEXT_STANDUP_IS_DONE = configs['TEXT_STANDUP_IS_DONE']
TEXT_NO_USER = configs['TEXT_NO_USER']
TEXT_CHANNEL_MESSAGE = configs['TEXT_CHANNEL_MESSAGE']
TEXT_NEW_DAY = configs['TEXT_NEW_DAY']

SLACK_COMMON_CHANNEL = configs['SLACK_COMMON_CHANNEL']
