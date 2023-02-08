
from datetime import timedelta
from pathlib import Path

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
SECRET_KEY = os.getenv('SECRET_KEY')
print("Secret key ", SECRET_KEY)


# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True


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
    'safedelete',
    
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

SOCIALACCOUNT_PROVIDERS = {
       'google': {
        'APP': 'google',
        'KEY': os.getenv('GOOGLE_KEY'),
        'SECRET': os.getenv('GOOGLE_SECRET'),
    },

    'facebook': {
        'APP': 'facebook',
        'KEY': os.getenv('FACEBOOK_KEY'),
        'SECRET': os.getenv('FACEBOOK_SECRET'),
    },
}

ALLOWED_HOSTS = ['localhost','Sodyam.pythonanywhere.com','127.0.0.1']

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

"""

'SERIALIZERS': {
    'user_create' : 'authentication.serializers.UserCreateSerializer',
    'user' : 'authentication.serializers.UserCreateSerializer',
    'user_delete' : 'djoser.serializers.UserDeleteSerializer',

    }
"""

#Djoser settings
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '/activate/{uid}/{token}',
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



# CORS HEADERS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': os.getenv('DB_ENGINE','django.db.backends.sqlite3'),
		'NAME':  os.getenv('DB_NAME',os.path.join(BASE_DIR, "db.sqlite3")),  
		'USER': os.getenv('DB_USER','root'),
		'PASSWORD': os.getenv('DB_PASSWORD','root'),
		'HOST': os.getenv('DB_HOST','localhost'),
		'PORT': os.getenv('DB_PORT','3306')
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

AUTH_USER_MODEL = 'authentication.User'
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_ALLOWED_HOSTS = ["localhost","127.0.0.1"]


#Email sending Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST =  os.getenv('EMAIL_HOST')
EMAIL_USE_TLS =os.getenv('EMAIL_USE_TLS')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
print("Email :",EMAIL_HOST_USER)

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
print("Password :",EMAIL_HOST_PASSWORD)


NAME = "VOTIFY APP"


#Add docker configuration 


DEBUG = int(os.getenv("DEBUG", default=1))


'''
{
  "username": "MARIUS",
  "email": "yaomariussodokin@gmail.com",
  "first_name": "Yao Marius",
  "last_name": "SODOKIN",
  "address": "Abomey Calavi",
  "phone": "+22990500075",
  "password": "Sody@m/9050",
  "re_password": "Sody@m/9050"
}

{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NjMwMTI5MywianRpIjoiY2U5Y2FjNDExODczNGVmNjg0MzQ5OGEwZGNhZjZlMmEiLCJ1c2VyX2lkIjoieWFvbWFyaXVzc29kb2tpbkBnbWFpbC5jb20ifQ.arHK7sMQss8FchHD7oDakQqisH5NZ9r0XK6AerJ9qAU",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc1OTU1NjkzLCJqdGkiOiIxOGM3MWY1NzE3OTQ0MWJjYTdhNDZmYzhmNTU5M2I0OSIsInVzZXJfaWQiOiJ5YW9tYXJpdXNzb2Rva2luQGdtYWlsLmNvbSJ9.b3GWEE9wNzV3RnUpYmgEDnEtHAJhsCLv6zAhG6fklV8"
}


'''



