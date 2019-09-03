"""

IMPORTANT NOTE:

This file could be outdated, please compare it with the template inside the Ansible playbooks

"""


import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = FILL_ME

GH_CLIENT_ID = FILL_ME
GH_CLIENT_SECRET = FILL_ME

GL_CLIENT_ID = FILL_ME
GL_CLIENT_SECRET = FILL_ME

MEETUP_CLIENT_ID = FILL_ME
MEETUP_CLIENT_SECRET = FILL_ME

ES_IN_HOST = FILL_ME # ELASTIC_CONTAINER_NAME
ES_IN_PORT = FILL_ME # ELASTIC_PORT
ES_IN_PROTO = FILL_ME # ELASTIC_PROTOCOL

ES_ADMIN_PSW = FILL_ME

KIB_IN_HOST = FILL_ME # KIBANA_CONTAINER_NAME
KIB_IN_PORT = FILL_ME # kibana_port
KIB_IN_PROTO = FILL_ME # kibana_protocol
KIB_PATH = FILL_ME # /kibana
KIB_OUT_URL = FILL_ME #  'https://localhost:port/KIB_PATH'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'CauldronApp',
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

ROOT_URLCONF = 'Cauldron2.urls'

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

WSGI_APPLICATION = 'Cauldron2.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': FILL_ME, # cauldron
        'USER': FILL_ME, # grimoirelab
        'PASSWORD': FILL_ME,
        'HOST': FILL_ME, # DB_CONTAINER_NAME
        'PORT': FILL_ME, # 3306
        'OPTIONS': {
            'sql_mode': 'traditional'
        }
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
