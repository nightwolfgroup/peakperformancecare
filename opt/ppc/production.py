from pathlib import Path
from django.contrib.messages import constants as messages

SECRET_KEY = 'e)l3_j_9g4$l34n9te%ayk%xd7(d$u+x)1xz6frpor8u#zy03#'

DEBUG = False

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ['peakperformancecare.com', 'www.peakperformancecare.com']


# Application definition

INSTALLED_APPS = [
    # Wagtail Applications
    'wagtail.contrib.forms',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'django.contrib.sitemaps',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    # Third-party Applications
    'modelcluster',
    'taggit',
    'wagtail_color_panel',
    'wagtailmenus',
    'wagtailmetadata',
    'wagtailfontawesome',
    'autoslug',
    'robots',
    # Django Applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Developer Initiated Applications
    'about.apps.AboutConfig',
    'blocks.apps.BlocksConfig',
    'blog.apps.BlogConfig',
    'careers.apps.CareersConfig',
    'contacts.apps.ContactsConfig',
    'core.apps.CoreConfig',
    'education.apps.EducationConfig',
    'regulatory.apps.RegulatoryConfig',
    'services.apps.ServicesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'ppc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/opt/ppc/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'ppc.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ppcdb',
        'USER': 'ppcdbuser',
        'PASSWORD': 'hI6eY5rI6jM8uM0vQ4dW5wW5k',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = '/var/cache/ppc/static/'
STATICFILES_DIRS = [
    '/opt/ppc/ppc/static/'
]


# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/opt/ppc/media/'


# Messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.INFO: 'info',
    messages.WARNING: 'warning'
}


# Wagtail Configuration

WAGTAIL_SITE_NAME = 'Peak Performance Care Physical Therapy'


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s: '
                      '%(message)s',
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.'
                     'TimedRotatingFileHandler',
            'filename': '/var/log/ppc/'
                        'django.log',
            'when': 'midnight',
            'backupCount': 60,
            'formatter': 'default',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}


# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.'
                   'FileBasedCache',
        'LOCATION': '/var/cache/ppc/cache',
    }
}
