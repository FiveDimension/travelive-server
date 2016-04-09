# #coding: utf-8
#
# import httplib2
# from functools import wraps
# import json
# from urllib import urlencode
# from sysconf import settings
#
#
# class DirectHttp(httplib2.Http):
#     def __init__(self, timeout=300, content_processor="", *args, **kwargs):
#         super(DirectHttp, self).__init__(timeout=timeout, *args, **kwargs)
#         self.content_processor = content_processor
#
#     def request(self, url, ttl=600, *args, **kwargs):
#         def wrapper(url, *args, **kwargs):
#             kwargs.pop('cache_ttl')
#
#             # add gzip forcelly
#             if not 'headers' in kwargs:
#                 headers = {"Accept-Encoding": "gzip, identity", 'cache-control': 'no-cache'}
#             else:
#                 headers = kwargs.pop('headers')
#             if "Accept-Encoding" not in headers:
#                 headers["Accept-Encoding"] = "gzip, identity"
#             elif not headers["Accept-Encoding"] or 'gzip' not in headers["Accept-Encoding"]:
#                 headers["Accept-Encoding"] = ",".join([
#                     headers["Accept-Encoding"], "gzip"
#                 ])
#
#             # all method use uppercase
#             method = kwargs.pop('method').upper() if 'method' in kwargs else 'GET'
#             resp, content = super(DirectHttp, self).request(url,
#                                                             headers=headers,
#                                                             method=method,
#                                                             *args,
#                                                             **kwargs)
#             if self.content_processor:
#                 return resp, self.content_processor(content)
#             else:
#                 return resp, content
#
#         return wrapper(url, cache_ttl=ttl, *args, **kwargs)
#
#     def osg_request(self, url, ttl=600, osg_token=settings.OSG_TOKEN, *args, **kwargs):
#         osg_kwargs = {
#             "access_token": osg_token,
#             "request_body": urlencode(json.dumps(kwargs))
#         }
#         return self.request(url, ttl, *args, **osg_kwargs)
#
#     @staticmethod
#     def json(*args, **kwargs):
#         def _decorate(func):
#             @wraps(func)
#             def wrapped(*args, **kwargs):
#                 resp, content = func(*args, **kwargs)
#                 if int(resp.status) == 200:
#                     return json.loads(content)
#                 else:
#                     return None
#             return wrapped
#         return _decorate
#
#
# if __name__ == '__main__':
#     @DirectHttp.json()
#     def test():
#         a = DirectHttp()
#         return a.request("")
#
#     print test()