from pathlib import Path
import os
import sys


# ============================================================
# BASE DIR
# ============================================================

if getattr(sys, 'frozen', False):

    # Dossier interne temporaire de PyInstaller
    BASE_DIR = Path(sys._MEIPASS)

    # Dossier réel où se trouve launcher.exe
    APP_DIR = Path(sys.executable).resolve().parent

else:

    # Mode développement
    BASE_DIR = Path(__file__).resolve().parent.parent
    APP_DIR = BASE_DIR


# ============================================================
# WEASYPRINT
# ============================================================

WEASYPRINT_BASEURL = BASE_DIR


# ============================================================
# DOSSIER DES DONNÉES PERSISTANTES
# ============================================================

DATA_DIR = APP_DIR / "DATA"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = 'django-insecure-eem!i$u8-9&hle@*et@n%guwauyx%s3*5q0(k9^73svi9#82pq'

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]


# ============================================================
# AUTHENTIFICATION
# ============================================================

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'gestion',
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# URL / WSGI
# ============================================================

ROOT_URLCONF = 'facturation.urls'

WSGI_APPLICATION = 'facturation.wsgi.application'


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [

    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates'
        ],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]


# ============================================================
# DATABASE SQLITE
# ============================================================

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        # IMPORTANT :
        # La base reste à côté de launcher.exe
        # et non dans _internal
        'NAME': DATA_DIR / 'db.sqlite3',
    }
}


# ============================================================
# PASSWORD VALIDATORS
# ============================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator'
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator'
    },

    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]


# ============================================================
# INTERNATIONALISATION
# ============================================================

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Africa/Dakar'

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC
# ============================================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# MEDIA
# ============================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = DATA_DIR / "media"

MEDIA_ROOT.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# WEASYPRINT
# ============================================================

os.environ["GIO_USE_VFS"] = "local"

WEASYPRINT_BASEURL = BASE_DIR


# ============================================================
# DEFAULT PK
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# STATIC STORAGE
# ============================================================

STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"
)