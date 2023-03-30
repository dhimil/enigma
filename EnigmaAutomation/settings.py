"""
Django settings for EnigmaAutomation project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import glob
from os.path import join
import json
from pathlib import Path
import os
import time
import random

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "abc"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "bootprocess.apps.BootprocessConfig",
    "social_django",
    "Access",
    "rest_framework",
    "cid.apps.CidAppConfig",
]
CID_GENERATE = True
CID_GENERATOR = lambda: f"{time.time()}-{random.random()}"
CID_HEADER = "X_CORRELATION_ID"
CID_GENERATE = True
CID_CONCATENATE_IDS = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "cid.middleware.CidMiddleware",
]

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "social_core.pipeline.debug.debug",
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    # Verifies that the social association can be disconnected from the current
    # user (ensure that the user login mechanism is not compromised by this
    # disconnection).
    # 'social.pipeline.disconnect.allowed_to_disconnect',
    # Collects the social associations to disconnect.
    "social_core.pipeline.disconnect.get_entries",
    # Revoke any access_token when possible.
    "social_core.pipeline.disconnect.revoke_tokens",
    # Removes the social associations.
    "social_core.pipeline.disconnect.disconnect",
)

ROOT_URLCONF = "EnigmaAutomation.urls"

template_dirs = glob.glob(join(BASE_DIR, "Access", "access_modules", "*", "templates"))
template_dirs.extend(glob.glob(join(BASE_DIR, "templates")))

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": template_dirs,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "Access.context_processors.add_variables_to_context",
            ],
        },
    },
]

WSGI_APPLICATION = "EnigmaAutomation.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DECLINE_REASONS = json.load(
    open(
        "constants.json",
    )
)["declineReasons"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "public/")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


with open("config.json") as data_file:
    data = json.load(data_file)


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = data["googleapi"]["SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"]
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = data["googleapi"]["SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"]
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login/'

if data["background_task_manager"]["type"] == "celery":
    background_task_manager_config = data["background_task_manager"]["config"]
    CELERY_BROKER_URL = background_task_manager_config["broker"]
    CELERY_RESULT_BACKEND = background_task_manager_config["backend"]

    if background_task_manager_config["need_monitoring"]:
        INSTALLED_APPS.append(background_task_manager_config["monitoring_apps"])

USER_STATUS_CHOICES = [
    ("1", "active"),
    ("2", "offboarding"),
    ("3", "offboarded"),
]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {}
if data["database"]["engine"] == "mysql":
    DATABASES["default"] = {
        "ENGINE": "mysql.connector.django",
        "CONN_MAX_AGE": 0,
        "NAME": data["database"]["dbname"],
        "USER": data["database"]["username"],
        "PASSWORD": data["database"]["password"],
        "HOST": data["database"]["host"],
        "PORT": data["database"]["port"],
        'OPTIONS': {
            "auth_plugin": "mysql_native_password",
            'charset': 'utf8mb4',
        }
    }
elif data["database"]["engine"] == "sqlite3":
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/db.sqlite3",
    }
else:
    raise Exception("Database engine %s not recognized" % data["database"]["engine"])

PERMISSION_CONSTANTS = {"DEFAULT_APPROVER_PERMISSION": "ACCESS_APPROVE"}

DEFAULT_ACCESS_GROUP = "default_access_group"
MAIL_APPROVER_GROUPS = data["enigmaGroup"]["MAIL_APPROVER_GROUPS"]

ACCESS_APPROVE_EMAIL = data["emails"]["access-approve"]

ACCESS_MODULES = data["access_modules"]

AUTOMATED_EXEC_IDENTIFIER = "automated-grant"

current_log_level = 'DEBUG'
logging_apps = ["django.request", "inventory", "Access", "bootprocess"]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "{\"meta\":{\"timestamp\":\"%(asctime)s.%(msecs)03dZ\",\"component\":\"django\",\"application\":\"enigma\",\"team\":\"core\"},\"log\":{\"kind\":\"ENIGMA_APP\",\"dynamic_data\":\"[%(name)s:%(funcName)s:%(lineno)s] --- %(message)s\",\"level\":\"%(levelname)s\"}}",
            'datefmt': "%Y-%m-%dT%H:%M:%S"
        }
    },
    'handlers': {
        'file': {
            'level': current_log_level,
            'class': 'logging.FileHandler',
            'filename': '/ebs/logs/enigma.log',
            'formatter': 'verbose',
        },
        "console": {
            "level": current_log_level,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {},
}
for each_app in logging_apps:
    LOGGING["loggers"][each_app] = {
        "handlers": ["console"],
        "level": current_log_level,
        "propagate": True,
        "formatter": "verbose",
    }