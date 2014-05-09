"""
Django settings for studyplan project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4a9s4wn^4np*@1i+j!1*2clm^36zo=dgu5-&0wzt20jujd()cn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #'south',
    'django_summernote',
    'jfu',

    'board',
    'core',
    'account',
    'school',
    'tag',
    'event',
    'file',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'studyplan.urls'

WSGI_APPLICATION = 'studyplan.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'kr-ko'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = '/account/sign_in/'
LOGOUT_URL = '/account/sign_out/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'multiuploader/templates'),
)

if DEBUG:
    MEDIA_URL = '/media/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static-only')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

#######################
# Comment
#######################

COMMENTS_APP = 'threadedcomments'

################################
# Summernote configuration
################################

SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': False,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Change editor size
    'width': '100%',
    'height': '480',

    # Set editor language/locale
    #'lang': 'en-US',
    'lang': 'ko-KR',

    # Customize toolbar buttons
    'toolbar': [
        ['style', ['style']],
        ['style', ['bold', 'italic', 'underline', 'clear']],
        ['para', ['ul', 'ol', 'height']],
        ['insert', ['link']],
    ],

    # Set `upload_to` function for attachments.
    #'attachment_upload_to': my_custom_upload_to_func(),

    # Set custom storage class for attachments.
    #'attachment_storage_class': 'my.custom.storage.class.name',
}
