{% if cookiecutter.use_sentry == 'y' -%}
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
{% if cookiecutter.use_celery == 'y' -%}
from sentry_sdk.integrations.celery import CeleryIntegration
{% endif %}
{% endif -%}
from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["{{ cookiecutter.domain_name }}"])

# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"] = env.db("DATABASE_URL")  # noqa F405
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405
DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-use-sessions
CSRF_USE_SESSIONS = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)

{% if cookiecutter.cloud_provider != 'None' -%}
# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ["storages"]  # noqa F405
{%- endif -%}
{% if cookiecutter.cloud_provider == 'AWS' %}
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME")
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_QUERYSTRING_AUTH = False
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate"
}
#  https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_DEFAULT_ACL = None
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_REGION_NAME = env("DJANGO_AWS_S3_REGION_NAME", default=None)
{% elif cookiecutter.cloud_provider == 'GCP' %}
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = env("DJANGO_GCP_STORAGE_BUCKET_NAME")
GS_DEFAULT_ACL = "publicRead"
{% endif -%}

{% if cookiecutter.cloud_provider != 'None' or cookiecutter.use_whitenoise == 'y' -%}
# STATIC
# ------------------------
{% endif -%}
{% if cookiecutter.use_whitenoise == 'y' -%}
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
{% elif cookiecutter.cloud_provider == 'AWS' -%}
STATICFILES_STORAGE = "config.settings.production.StaticRootS3Boto3Storage"
STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/"
{% elif cookiecutter.cloud_provider == 'GCP' -%}
STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
{% endif -%}

# MEDIA
# ------------------------------------------------------------------------------
{%- if cookiecutter.cloud_provider == 'AWS' %}
# region http://stackoverflow.com/questions/10390244/
# Full-fledge class: https://stackoverflow.com/a/18046120/104731
from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


# endregion
DEFAULT_FILE_STORAGE = "config.settings.production.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/"
{%- elif cookiecutter.cloud_provider == 'GCP' %}
MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
MEDIA_ROOT = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
{%- endif %}

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]["OPTIONS"]["loaders"] = [  # noqa F405
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env(
    "DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL,
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX", default="[Django] "
)
EMAIL_HOST = env('DJANGO_EMAIL_HOST')
EMAIL_HOST_USER = env('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('DJANGO_EMAIL_USE_TLS', default=True)
EMAIL_PORT = env('DJANGO_EMAIL_PORT', default=587)

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env("DJANGO_ADMIN_URL")

{% if cookiecutter.use_whitenoise == 'y' -%}
# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#enable-whitenoise
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa F405

{% endif %}
{%- if cookiecutter.use_compressor == 'y' -%}
# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = env.bool("COMPRESS_ENABLED", default=True)
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL{% if cookiecutter.use_whitenoise == 'y' or cookiecutter.cloud_provider == 'None' %}  # noqa F405{% endif %}
{% endif %}
{%- if cookiecutter.use_whitenoise == 'n' -%}
# Collectfast
# ------------------------------------------------------------------------------
# https://github.com/antonagestam/collectfast#installation
INSTALLED_APPS = ["collectfast"] + INSTALLED_APPS  # noqa F405
{% endif %}
# LOGGING
# ------------------------------------------------------------------------------
# Remove debug requirement from console handler
del LOGGING["handlers"]["console"]["filters"]

{% if cookiecutter.use_sentry == 'y' -%}
# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[
        DjangoIntegration(),
        {% if cookiecutter.use_celery == 'y' -%}
        CeleryIntegration(),
        {% endif -%}
    ],
)

{% endif -%}
# Recaptcha
# ------------------------------------------------------------------------------
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")

# Your stuff...
# ------------------------------------------------------------------------------
