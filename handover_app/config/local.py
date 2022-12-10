from .base import *
import environ

env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
DATABASES = {
    'default': env.db(),
}

#########################################
# Static files (CSS, JavaScript, Images)#
#########################################
STATIC_URL = '/static/'

################
# Media files #
################
MEDIA_URL = '/media/'