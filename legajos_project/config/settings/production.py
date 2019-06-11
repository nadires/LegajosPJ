# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sistemalegajos',
        'USER': 'admin',
        'PASSWORD': 'infoper123asd',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}