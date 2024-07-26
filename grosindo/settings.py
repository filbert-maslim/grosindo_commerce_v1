"""
Django settings for grosindo project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-bhxjhlucp&=vj7lnrs^1nc2@bs^1@2i0#bwtbh1h4^!1-i_2de'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    
    #Allauth apps
    'allauth.usersessions',
    'allauth',
    'allauth.account',
    'django.contrib.humanize',
    
    #Dependencies apps
    'phonenumber_field',

    #Custom apps
    'category',
    'accounts',
    'store',
    'cart',
    'orders',
    # 'products'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    #Allauth middlewear
    'allauth.usersessions.middleware.UserSessionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'grosindo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
                'cart.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'grosindo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR/'static'
STATICFILES_DIRS = [
    'grosindo/static'
]

# Media files configuratoins
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Configure django message to send Error and Success notification to users
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR:'danger',
}

#SMTP configuration for email
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=465
EMAIL_HOST_USER=os.getenv('gmail_email')
EMAIL_HOST_PASSWORD=os.getenv('gmail_email_pass')
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True

#Phone number config
PHONENUMBER_DEFAULT_REGION = "ID"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"
PHONENUMBER_DB_FORMAT = "NATIONAL"

# Django allauth config
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CHANGE_EMAIL  = True
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_LOGIN_BY_CODE_MAX_ATTEMPTS = 5
LOGIN_REDIRECT_URL = 'dashboard'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'phone_number'
ACCOUNT_USERNAME_MIN_LENGTH = 10
ACCOUNT_USERNAME_VALIDATORS = (
    'phonenumber_field.validators.validate_international_phonenumber',
    )

AUTH_USER_MODEL = 'accounts.User'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'account_login'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # existing backend
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_FORMS = {
    'signup': 'accounts.forms.AllauthRegistrationForm',
    }

ACCOUNT_ADAPTER = (
    # Set Allauth account adapters to our modified adapters
    "accounts.adapters.AccountAdapter"
    )

# User defined variables
MAX_USER_ADDRESS_CNT = 3

TAX_RATE = 0

ECOMMERCE_PLATFORM = (
    ("Shopee", "Shopee"),
    ("Tiktok", "Tiktok"),
)