#!/usr/bin/env python
#coding: UTF-8

'''
Created on Oct 12, 2012

@author: oliveagle
@mail:     oliveagle@gmail.com
'''
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.encoding import smart_unicode
from django import http
try:
    import json
except:
    from django.utils import simplejson as json
import logging


def render_to_response(context):
    "Returns a JSON response containing 'context' as payload"
    return get_json_response(convert_context_to_json(context))


def get_json_response(content, **httpresponse_kwargs):
    "Construct an `HttpResponse` object."
    return http.HttpResponse(content,
                             content_type='application/json',
                             **httpresponse_kwargs)


def convert_context_to_json(context):
    "Convert the context dictionary into a JSON object"
    # Note: This is *EXTREMELY* naive; in reality, you'll need
    # to do much more complex handling to ensure that arbitrary
    # objects -- such as Django model instances or querysets
    # -- can be serialized as JSON.
    return json.dumps(context)


class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return render_to_response(context)

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return get_json_response(content, **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return convert_context_to_json(context)

# view decorators

def render_with(template_name):
    """
    Renders the view wrapped by this decorator with the given template.  The
    view should return the context to be used in the template, or an
    HttpResponse.

    If the view returns an HttpResponseRedirect, the decorator will redirect
    to the given URL, or to request.REQUEST['next'] (if it exists).
    """
    def render_with_decorator(view_func):
        def wrapper(*args, **kwargs):
            request = args[0]   # 3
            response = view_func(*args, **kwargs)

            if isinstance(response, HttpResponse):
                if isinstance(response, HttpResponseRedirect) and \
                        'next' in request.REQUEST:
                    return HttpResponseRedirect(request.REQUEST['next'])
                else:
                    return response
            else:
                # assume response is a context dictionary
                context = response
                response = TemplateResponse(request, template_name, context)
                return response
        return wrapper
    return render_with_decorator

def json_response_view(logger=None, log_level=logging.ERROR):
    """
    @param logger: instance of logging.Logger
    @param log_level: logging level, default: logging.ERROR

    @param _render2response:  render成Django Response, 否则直接返回function的结果,
        这样可以在同样的app中直接调用这个view function 但是却不render.
        这个参数直接添加在调用被修饰的func里 e.g.:
            res = view_func(a=1, _render2response=False)
    返回json结果的decorator.

    有错误的时候返回的结果:
        {'error':1,    # 0 没有错误， 1 有错但未知， xxxx， 已知错误代码
        'message':'',    # 错误信息, 没有错误时为空
        'request': '',     # 有错误的时候会返回错误的request.path
        'success': False,
        }
    @view_dec.json_response_view()
    def a_view_function(request):
        pass
    没有错误返回:
        {'error': 0, 'data': '', 'message': '', 'success': True}

    # view function 报错，但是没有在已知错误列表中
    {"message": "\u4e2d\u6587\u4e5f\u6ca1\u6709\u95ee\u9898",
        "request": "/share_to_sina_weibo/", "error": 1, 'success': False}

    # view function raise errors.EMPTY_INPUT
    {"message": "\u8f93\u5165\u4e3a\u7a7a",
        "request": "/share_to_sina_weibo/", "error": 20002, 'success': False}
    """
    if not logger or not isinstance(logger, logging.Logger):
        logger = logging

    def render_with_decorator(view_func):
        def wrapper(*args, **kwargs):
            assert len(args)>=1 and isinstance(args[0], HttpRequest), \
                'request should be the first param of the decorated function'

            # pop out _render2response if we pass it as a keyword arguments in
            # decorated function
            _render2response = True
            if '_render2response' in kwargs:
                _render2response = kwargs.pop("_render2response")

            try:
                res = {'error': 0, 'message': '', 'success': False}
                request = args[0]   # request always the first argument
                res['data'] = view_func(*args, **kwargs)
                res['success'] = True
            except Exception, e:
                # res['error']
                res['error'] = e.code if hasattr(e, 'code') else 1

                # res['message']
                if hasattr(e, 'message'):
                    res['message'] = smart_unicode(e.message)
                else:
                    res['message'] = smart_unicode(e)

                # res['request']
                res['request'] = smart_unicode("?".join([request.path, request.META.get('QUERY_STRING')]))

                # log in different level
                if log_level in [logging.ERROR, logging.CRITICAL]:
                    logger.exception(res)
                else:
                    logger.log(log_level, res)
            finally:
                # render result
                if _render2response == False:
                    # return response of the function directly if _render2response
                    # is been set to False.
                    return res

                if isinstance(res, HttpResponse):
                    if isinstance(res, HttpResponseRedirect) and \
                            'next' in request.REQUEST:
                        return HttpResponseRedirect(request.REQUEST['next'])
                    else:
                        return res
                else:
                    # assume res is a context dictionary
                    return render_to_response(res)
        return wrapper
    return render_with_decorator



def json_response_view_no_schema(logger=None, log_level=logging.ERROR):
    """
    @param logger: instance of logging.Logger
    @param log_level: logging level, default: logging.ERROR

    @param _render2response:  render成Django Response, 否则直接返回function的结果,
        这样可以在同样的app中直接调用这个view function 但是却不render.
        这个参数直接添加在调用被修饰的func里 e.g.:
            res = view_func(a=1, _render2response=False)
    返回json结果的decorator.

    有错误的时候返回的结果:
        {'error':1,    # 0 没有错误， 1 有错但未知， xxxx， 已知错误代码
        'message':'',    # 错误信息, 没有错误时为空
        'request': '',     # 有错误的时候会返回错误的request.path
        'success': False,
        }
    @view_dec.json_response_view()
    def a_view_function(request):
        pass
    没有错误返回:
        {'error': 0, 'data': '', 'message': '', 'success': True}

    # view function 报错，但是没有在已知错误列表中
    {"message": "\u4e2d\u6587\u4e5f\u6ca1\u6709\u95ee\u9898",
        "request": "/share_to_sina_weibo/", "error": 1, 'success': False}

    # view function raise errors.EMPTY_INPUT
    {"message": "\u8f93\u5165\u4e3a\u7a7a",
        "request": "/share_to_sina_weibo/", "error": 20002, 'success': False}
    """
    if not logger or not isinstance(logger, logging.Logger):
        logger = logging

    def render_with_decorator(view_func):
        def wrapper(*args, **kwargs):
            assert len(args)>=1 and isinstance(args[0], HttpRequest), \
                'request should be the first param of the decorated function'

            # pop out _render2response if we pass it as a keyword arguments in
            # decorated function
            _render2response = True
            if '_render2response' in kwargs:
                _render2response = kwargs.pop("_render2response")

            try:
                request = args[0]   # request always the first argument
                #res['data'] = view_func(*args, **kwargs)
                #res['success'] = True
                res = view_func(*args, **kwargs)
            except Exception, e:
                # res['error']
                res = {'error': 0, 'message': '', 'success': False}
                res['error'] = e.code if hasattr(e, 'code') else 1

                # res['message']
                if hasattr(e, 'message'):
                    res['message'] = smart_unicode(e.message)
                else:
                    res['message'] = smart_unicode(e)

                # res['request']
                res['request'] = smart_unicode("?".join([request.path, request.META.get('QUERY_STRING')]))

                # log in different level
                if log_level in [logging.ERROR, logging.CRITICAL]:
                    logger.exception(res)
                else:
                    logger.log(log_level, res)
            finally:
                # render result
                if _render2response == False:
                    # return response of the function directly if _render2response
                    # is been set to False.
                    return res

                if isinstance(res, HttpResponse):
                    if isinstance(res, HttpResponseRedirect) and \
                            'next' in request.REQUEST:
                        return HttpResponseRedirect(request.REQUEST['next'])
                    else:
                        return res
                else:
                    # assume res is a context dictionary
                    return render_to_response(res)
        return wrapper
    return render_with_decorator


class HttpAjaxResponse(HttpResponse):

    def __init__(self, content={}, mimetype=None, status=None, content_type='application/json'):
        content = json.dumps(content)
        super(HttpAjaxResponse, self).__init__(content=content,
                                               mimetype=mimetype, status=status, content_type=content_type)

