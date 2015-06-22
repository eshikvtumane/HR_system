#-*- coding:utf8 -*-
"""
Django settings for HR_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#импортируем модуль с настройками для celery
import celeryconfig


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_ed%n*nd*r17zmx(76ii5a1%xda4z7l5%)j$4-h%b)h@szek@&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG404 = False

TEMPLATE_DEBUG = False
THUMBNAIL_DEBUG = True
DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': os.path.join(BASE_DIR, '/static/js/jquery/jquery-2.1.3.min.js')
}

# ссылка на производственный календарь
PRODUCTION_CALENDAR = 'http://basicdata.ru/api/json/calend/'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

LOGIN_URL = 'users:login'
LOGOUT_URL = 'users:logout'
LOGIN_REDIRECT_URL = 'users:login'


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrapform',
    'sorl.thumbnail',
    'pure_pagination',
    #'debug_toolbar',
    'main',
    'applicants',
    'vacancies',
    'administration',
    'users',
    'reports',
    'events',
    'email_constructor',
    'swampdragon',
    'notifications',
    'employees'

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS=(
    "django.core.context_processors.request",
    'django.contrib.auth.context_processors.auth'
)





ROOT_URLCONF = 'HR_project.urls'

WSGI_APPLICATION = 'HR_project.wsgi.application'


# SwampDragon settings
SWAMP_DRAGON_CONNECTION = ('swampdragon.connections.sockjs_connection.DjangoSubscriberConnection', '/data')
DRAGON_URL='http://localhost:9999/'


PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 20,
    'MARGIN_PAGES_DISPLAYED': 2,
}

GRAPPELLI_ADMIN_TITLE = 'ИС АПП - административная панель'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


'''if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hr_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Vladivostok'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR,'../collectstatic')
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,'templates'),

)   

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
    os.path.join(BASE_DIR,'vacancies/static'),
    os.path.join(BASE_DIR,'applicants/static'),
    os.path.join(BASE_DIR,'main/static'),
    os.path.join(BASE_DIR,'reports/static'),
    os.path.join(BASE_DIR,'administration/static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# email connect settings
EMAIL_SENDER = 'hr@riavs.ru'
EMAIL_HOST = ''
EMAIL_HOST_PORT = ''
EMAIL_LOGIN = ''
EMAIL_PASSWORD = ''



