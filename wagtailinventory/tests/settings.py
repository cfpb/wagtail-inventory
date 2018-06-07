from __future__ import absolute_import, unicode_literals

import django
import wagtail

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'not needed'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'wagtailinventory.sqlite',
    },
}

if wagtail.VERSION >= (2, 0):
    WAGTAIL_APPS = (
        'wagtail.contrib.forms',
        'wagtail.contrib.modeladmin',
        'wagtail.contrib.settings',
        'wagtail.tests.testapp',
        'wagtail.admin',
        'wagtail.core',
        'wagtail.documents',
        'wagtail.images',
        'wagtail.sites',
        'wagtail.users',
    )

    WAGTAIL_MIDDLEWARE = (
        'wagtail.core.middleware.SiteMiddleware',
    )

    WAGTAILADMIN_RICH_TEXT_EDITORS = {
        'default': {
            'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea'
        },
        'custom': {
            'WIDGET': 'wagtail.tests.testapp.rich_text.CustomRichTextArea'
        },
    }
else:
    WAGTAIL_APPS = (
        'wagtail.contrib.modeladmin',
        'wagtail.contrib.settings',
        'wagtail.tests.testapp',
        'wagtail.wagtailadmin',
        'wagtail.wagtailcore',
        'wagtail.wagtaildocs',
        'wagtail.wagtailforms',
        'wagtail.wagtailimages',
        'wagtail.wagtailsites',
        'wagtail.wagtailusers',
    )

    WAGTAIL_MIDDLEWARE = (
        'wagtail.wagtailcore.middleware.SiteMiddleware',
    )

    WAGTAILADMIN_RICH_TEXT_EDITORS = {
        'default': {
            'WIDGET': 'wagtail.wagtailadmin.rich_text.HalloRichTextArea',
        },
        'custom': {
            'WIDGET': 'wagtail.tests.testapp.rich_text.CustomRichTextArea'
        },
    }

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'taggit',

) + WAGTAIL_APPS + (
    'wagtailinventory',
    'wagtailinventory.tests.testapp',
)


if django.VERSION >= (1, 10):
    MIDDLEWARE = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ) + WAGTAIL_MIDDLEWARE
else:
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ) + WAGTAIL_MIDDLEWARE

STATIC_URL = '/static/'

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
                'django.template.context_processors.request',
            ],
            'debug': True,
        },
    },
]

WAGTAIL_SITE_NAME = 'Test Site'
