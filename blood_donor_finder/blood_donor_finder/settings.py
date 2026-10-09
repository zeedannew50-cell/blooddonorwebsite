"""
Settings for the Blood Donor Finder.

Data is stored in MongoDB (via pymongo), not Django's SQL ORM,
so the default SQL apps (admin, auth, sessions) are removed.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-insecure-key')
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'donors',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blood_donor_finder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'blood_donor_finder.wsgi.application'

# No SQL database - everything lives in MongoDB.
DATABASES = {}

# Paste your MongoDB connection string here, or set the MONGO_URI environment variable.
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB_NAME = 'blood_donor_finder'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
