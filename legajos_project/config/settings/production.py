# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '172.16.28.200']
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sistemalegajos',
        'USER': 'admin',
        'PASSWORD': 'infoper123asd',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
