import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRET_KEY = 'r%moc(s^43i5^$_f$7o5w&j32zvo4qh)3p(11nafj#zr(ssr4+'
DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
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

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'
DATABASES = {
    'default':{
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'kabu_100',
         'USER': '',
         'PASSWORD': '',
         'HOST': '127.0.0.1',
         'PORT': 3306,
    },
}

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

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'standard':{
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './logs/debug.log',
            'formatter':'standard',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter':'standard',
        },
    },
    'loggers': {
        'app.management.commands': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

#Yahoo Auth
YAHOO_LOGIN_URL = "https://login.yahoo.co.jp/config/login?.src=www&.done=https://www.yahoo.co.jp"
YAHOO_USER_ID = ""
YAHOO_PASSWORD = ""

#Yahoo Vip Download CSV
CSV_DIR = "./tmp/yahooCsv/"

#楽天証券 トレード履歴csv保管場所
RAKUTEN_TRADE_HISTORY_CSV_DIR = "./tmp/rakutenTradeHistoryCsv/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# メールサーバーへの接続設定
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'xxxx@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS = True
FROM_EMAIL = 'xxxx@gmail.com'
RECIPIENT_LIST = ['xxxx@gmail.com']

#local_settingsを読み込み
try:
    from .local_settings import *
except ImportError:
    pass