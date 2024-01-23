"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-b0itubj4*gv#(rn7c6#=mgw7@k6-d&0hq*vw8+2l#2#13c#vpu"

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
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


###############################################################################
##                                  CUSTOM                                   ##
###############################################################################

## Override django default settings


import os

## Custom Apps


def _add_app(manifest):
    def is_same_type(a, b):
        return type(a) == type(b)

    installed_apps = manifest.get("installed_apps", [])
    for app in installed_apps:
        if app not in INSTALLED_APPS:
            INSTALLED_APPS.append(app)

    # Merge overrides settings
    g = globals()
    for key, value in manifest.get("overrides", {}).items():
        if key in g and is_same_type(value, g[key]):
            if isinstance(value, list):
                g[key].extend(value)
            elif isinstance(value, tuple):
                g[key] += value
            elif isinstance(value, dict):
                g[key].update(value)
            elif isinstance(value, set):
                g[key].update(value)
        else:
            g[key] = value


# Misc
DJANGO_DEFAULT_SETTINGS = {
    "name": "misc",
    "overrides": {
        "DEBUG": True,
        "ALLOWED_HOSTS": ["*"],
        "MIDDLEWARE": [
            "django.middleware.gzip.GZipMiddleware",
        ],
        "DATABASES": {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "HOST": os.getenv("DB_HOST"),
                "NAME": os.getenv("DB_NAME"),
                "PORT": os.getenv("DB_PORT"),
                "USER": os.getenv("DB_USER"),
                "PASSWORD": os.getenv("DB_PASSWORD"),
                "DISABLE_SERVER_SIDE_CURSORS": True,
            },
        },
        "STATICFILES_DIRS": (BASE_DIR / "static",),
        "STATIC_ROOT": BASE_DIR / "staticfiles" / "static",
    },
}
_add_app(DJANGO_DEFAULT_SETTINGS)


# core
CORE_SETTINGS = {
    "name": "core",
    "installed_apps": ["core"],
}
_add_app(CORE_SETTINGS)


# Custom User Model
CUSTOM_USER_SETTINGS = {
    "name": "accounts",
    "installed_apps": ["accounts"],
    "overrides": {
        "AUTH_USER_MODEL": "accounts.CustomUser",
        "DEFAULT_USER_GROUP_NAME": "users",
    },
}
_add_app(CUSTOM_USER_SETTINGS)


# whitenoise
WHITENOISE_SETTINGS = {
    "name": "whitenoise",
    "overrides": {
        "STATICFILES_STORAGE": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "MIDDLEWARE": ["whitenoise.middleware.WhiteNoiseMiddleware"],
    },
}
_add_app(WHITENOISE_SETTINGS)


# django-compressor
DJANGO_COMPRESSOR_SETTINGS = {
    "name": "compressor",
    "installed_apps": [
        "compressor",
        "django.contrib.humanize",  # somehow required for django-compressor
    ],
    "overrides": {
        "COMPRESS_ENABLED": True,
        "COMPRESS_OFFLINE": True,
        "COMPRESS_ROOT": BASE_DIR / "static",
        "COMPRESS_PRECOMPILERS": (
            ("text/css", "django_libsass.SassCompiler"),
            ("text/x-scss", "django_libsass.SassCompiler"),
            ("text/x-sass", "django_libsass.SassCompiler"),
        ),
        "COMPRESS_FILTERS": {
            "css": [
                "compressor.filters.css_default.CssAbsoluteFilter",
                "compressor.filters.cssmin.CSSMinFilter",
            ],
            "js": ["compressor.filters.jsmin.JSMinFilter"],
        },
        "STATICFILES_FINDERS": [
            "compressor.finders.CompressorFinder",
            "django.contrib.staticfiles.finders.FileSystemFinder",
            "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        ],
    },
}
_add_app(DJANGO_COMPRESSOR_SETTINGS)


# django-allauth
DJANGO_ALLAUTH_SETTINGS = {
    "name": "django_allauth",
    "installed_apps": [
        "allauth",
        "allauth.account",
        "allauth.socialaccount",
        "allauth.socialaccount.providers.github",
        "allauth.socialaccount.providers.google",
    ],
    "overrides": {
        "AUTHENTICATION_BACKENDS": [
            # Needed to login by username in Django admin, regardless of `allauth`
            "django.contrib.auth.backends.ModelBackend",
            # `allauth` specific authentication methods, such as login by email
            "allauth.account.auth_backends.AuthenticationBackend",
        ],
        "MIDDLEWARE": [
            "allauth.account.middleware.AccountMiddleware",
        ],
    },
}
_add_app(DJANGO_ALLAUTH_SETTINGS)

# django-cors-headers
DJANGO_CORS_HEADERS_SETTINGS = {
    "name": "django_cors_headers",
    "installed_apps": ["corsheaders"],
    "overrides": {
        "CORS_ALLOW_ALL_ORIGINS": True,
        "CORS_ALLOW_METHODS": ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"],
        "CORS_ALLOW_HEADERS": [
            "accept",
            "accept-encoding",
            "authorization",
            "content-type",
            "dnt",
            "origin",
            "user-agent",
            "x-csrftoken",
            "x-requested-with",
        ],
        "MIDDLEWARE": [
            "corsheaders.middleware.CorsMiddleware",
        ],
    },
}
_add_app(DJANGO_CORS_HEADERS_SETTINGS)


# django-htmx
DJANGO_HTMX_SETTINGS = {
    "name": "django-htmx",
    "installed_apps": ["django_htmx"],
    "overrides": {
        "MIDDLEWARE": ["django_htmx.middleware.HtmxMiddleware"],
    },
}
_add_app(DJANGO_HTMX_SETTINGS)

### django-browser-reload
DJANGO_BROWSER_RELOAD_SETTINGS = {
    "name": "django-browser-reload",
    "installed_apps": ["django_browser_reload"],
    "overrides": {
        "MIDDLEWARE": ["django_browser_reload.middleware.BrowserReloadMiddleware"],
    },
}
_add_app(DJANGO_BROWSER_RELOAD_SETTINGS)
