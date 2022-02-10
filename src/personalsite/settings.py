import json
import os
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured(f"Please check your {setting}")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =  get_secret('DEBUG')

RECAPTCHA_SECRET_KEY = get_secret('RECAPTCHA_SECRET_KEY')

ALLOWED_HOSTS =  get_secret('ALLOWED_HOSTS')

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'personalsite.apps.MyAdminConfig', # replacing default admin config with my own to augment ordering
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sessions.backends.signed_cookies',
    'channels',
    'landingpage',
    'loan_calc',
    'newsreader',
    'tests'
]

if DEBUG: 

    MEDIA_ROOT = os.path.join(BASE_DIR,'media_product')
    MEDIA_URL = '/media_product/'
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR,'static')
    STATICFILES_DIRS = [] 

    INSTALLED_APPS.append('django_vite') 

    # Where ViteJS assets are built.
    DJANGO_VITE_ASSETS_PATH = os.path.join(BASE_DIR,'newsreader/frontend/newsreader/')
    STATICFILES_DIRS.append(DJANGO_VITE_ASSETS_PATH)

    # If use HMR or not.
    DJANGO_VITE_DEV_MODE = DEBUG
    DJANGO_VITE_DEV_SERVER_HOST = 'localhost'
    DJANGO_VITE_DEV_SERVER_PORT = '3000'
    # Include DJANGO_VITE_ASSETS_PATH into STATICFILES_DIRS to be copied inside
    # when run command python manage.py collectstatic

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'personalsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'landingpage/templates/landingpage'),
                os.path.join(BASE_DIR,'loan_calc/templates/loan_calc'), 
                os.path.join(BASE_DIR,'newsreader/templates/newsreader'),
                os.path.join(BASE_DIR,'weather/templates/weather'),
                ],
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

WSGI_APPLICATION = 'personalsite.wsgi.application'
ASGI_APPLICATION = 'personalsite.asgi.application'



CHANNEL_LAYERS = {
    'default': {
        ### Method 1: Via redis lab
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     "hosts": [
        #       'redis://h:<password>;@<redis Endpoint>:<port>' 
        #     ],
        # },

        ### Method 2: Via local Redis
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #      "hosts": [('127.0.0.1', 6379)],
        # },

        ### Method 3: Via In-memory channel layer
        ## Using this method.
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'personalsite',
        'USER': 'abdi',
        'PASSWORD': get_secret('DB_PASSWORD'),
    }
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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'abdinasir'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
# EMAIL_SSL_CERTFILE = '/etc/letsencrypt/live/abdinasirnoor.com-0001/cert.pem'
# EMAIL_SSL_KEYFILE = '/etc/letsencrypt/live/abdinasirnoor.com-0001/privkey.pem'
DEFAULT_FROM_EMAIL = 'Abdinasir <Abdinasir@abdinasirnoor.com>'

