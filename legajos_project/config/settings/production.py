# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'SistemaLegajos',
        'USER': 'postgres',
        'PASSWORD': '3578563',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}