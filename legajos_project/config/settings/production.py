# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'SistemaLegajos',
        'USER': 'admin',
        'PASSWORD': 'infoper123asd',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}