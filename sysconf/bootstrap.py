
ES_HOST = "http://10.2.25.107:8000"
INDEX = "travelive"
DESTINATION_TYPE = "destination"
VIEWPOINT_TYPE = "viewpoint"
USER_TYPE = "user"
STREAM_TYPE = "stream"

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
