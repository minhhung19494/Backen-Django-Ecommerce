'''Use this for production'''

from .base import *
import dj_database_url

DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS += [
    '*'
]
WSGI_APPLICATION = 'home.wsgi.prod.application'
SECRET_KEY= config('SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# WHiteNoise
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# S3 Storage
AWS_LOCATION = 'static'
AWS_ACCESS_KEY_ID ='AKIAVOQ3XIH7XECMMISK' 
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME ='minhhungbucket'
AWS_S3_CUSTOM_DOMAIN='%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {    
     'CacheControl': 'max-age=86400',
}
AWS_S3_REGION_NAME = 'ap-southeast-1'
DEFAULT_FILE_STORAGE = 'home.storage_backends.MediaStorage'
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
] 
STATIC_URL='https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, 'static')

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
STATICFILES_FINDERS = (           
    'django.contrib.staticfiles.finders.FileSystemFinder',    
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
AWS_DEFAULT_ACL = None

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://127.0.0.1:3000',
)

# STATIC_URL = '/static/'
# MEDIA_URL = '/media/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Stripe
STRIPE_PUBLIC_KEY = config('STRIPE_TEST_PUBLIC_KEY')
STRIPE_SECRET_KEY = config('STRIPE_TEST_SECRET_KEY')