import platform

current_hostname = platform.uname()[1].lower()

test_hostname_list = ['VMS05467']

is_test_env = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'travelive',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '10.3.6.208',
        'PORT': '3306',
    }
}

CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
        }
    }
}

# # CAS Setting
# CAS_SERVER_URL = "http://cas.uat.qa.nt.ctripcorp.com/caso/"
# CAS_LOGOUT_COMPLETELY = True
# CAS_IGNORE_REFERER = True
# CAS_REDIRECT_URL = "/"
# CAS_AUTO_CREATE_USERS = True
# CAS_GATEWAY = False
# CAS_RETRY_LOGIN = True
#
# LOGIN_URL = "/login/"
# LOGOUT_URL = "/logout/"
