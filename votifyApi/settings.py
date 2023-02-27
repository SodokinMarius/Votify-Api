
from datetime import timedelta
from pathlib import Path
import django

# base configuration of environnement variable loading
import os
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#The following config is important for sql database
import pymysql

pymysql.install_as_MySQLdb()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-0pp!9_m3d!x^il8kne274sz6*cijk6hq3&d$vxm690pc(zl&0^"
print("Secret key ", SECRET_KEY)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'votifyApp',
    'drf_yasg',
    'allauth',
    'allauth.account', # for basic authentication
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
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

ROOT_URLCONF = 'votifyApi.urls'


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

WSGI_APPLICATION = 'votifyApi.wsgi.application'


#Configuration des Providers social

GOOGLE_KEY='704829398857-2bl8dun6qvavhd9lgkko3157o9cot0fv.apps.googleusercontent.com'
GOOGLE_SECRET='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'


FACEBOOK_KEY='2177463709111231'
FACEBOOK_SECRET='d57e1945c9f4fadef7ce1be5cd025eed'

SOCIALACCOUNT_PROVIDERS = {
       'google': {
        'APP': 'google',
        'KEY': GOOGLE_KEY,
        'SECRET': GOOGLE_SECRET,
    },

    'facebook': {
        'APP': 'facebook',
        'KEY': FACEBOOK_KEY,
        'SECRET': FACEBOOK_SECRET,
    },
}

ALLOWED_HOSTS = ['localhost','votifyapp.pythonanywhere.com','127.0.0.1']

#Django Rest Framework strategy

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
     'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# django-rest-framework-simplejwt configuration to use the Authorization:


SIMPLE_JWT = {
    'USER_ID_FIELD': 'email',
    'AUTH_HEADER_TYPES': 'Bearer',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=24*60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.RefreshToken',
    )
}


#Swagger setting configuration
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

#Djoser Email config
EMAIL = {

    'FROM_EMAIL': 'votify.com',

}

#for allauth
AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]

#Djoser settings
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activation/<str:email>/<str:code>',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL' :True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION':True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION' : True,

    'USER_CREATE_PASSWORD_RETYPE' : True,
    'SET_USERNAME_RETYPE': True,


    'SET_PASSWORD_RETYPE' : True,
    'PASSWORD_RESET_CONFIRM_RETYPE':True,

    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND' : True,
    'USERNAME_RESET_SHOW_EMAIL_NOT_FOUND' : True,

    'SERIALIZERS': {
        'user_create' : 'authentication.serializers.UserCreateSerializer',
        'user' : 'djoser.serializers.UserSerializer',
        'current_user' : 'djoser.serializers.UserSerializer',
        'user_delete' : 'djoser.serializers.UserSerializer',

        },
    'EMAIL': EMAIL,

    'LOGIN_FIELD' : 'email'
}

APPEND_SLASH = False

# CORS HEADERS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
	'default': {

		'ENGINE': "django.db.backends.mysql",
		'NAME': "votifyAppDb",
		'USER': "votifyAdmin",
		'PASSWORD': "votify@admin",
		'HOST': "votifyapp.mysql.pythonanywhere-services.com",

  	     "OPTIONS": {

            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
            'charset': 'utf8mb4',
            "autocommit": True,
        },

		'PORT': 3306
		}


	}



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Africa/Porto-Novo'

USE_I18N = True

USE_TZ = True

from datetime import datetime
print(datetime.now())

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

'''Create the static root : python3 manage.py collectstatic'''
STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')

AUTH_USER_MODEL = 'authentication.User'
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_ALLOWED_HOSTS = ['localhost','votifyapp.pythonanywhere.com','127.0.0.1']


#Mailing service
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER="yaomariussodokin@gmail.com"
EMAIL_HOST_PASSWORD="beagvuxewtwwutib"


print("Password :",EMAIL_HOST_PASSWORD)


NAME = "VOTIFY APP"


#Add docker configuration


#DEBUG = int(os.getenv("DEBUG", default=0))
CURRENT_USER_ID = None

print("DEBUG ------------>",DEBUG)

