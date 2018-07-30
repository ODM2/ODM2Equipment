from odm2equipment.settings.base import *

DEBUG = True

INTERNAL_IPS = (
    '127.0.0.1',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = config["static_root"]
STATIC_URL = '/static/'

SITE_URL = ''
