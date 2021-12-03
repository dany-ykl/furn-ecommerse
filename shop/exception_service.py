import datetime
import functools
import inspect
import json
import traceback
from typing import Dict

from django.db import transaction
from django.http import JsonResponse
from django.views import View


JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}

def ret(json_object, status=200):
    """Отдает JSON ответ с правильными HTTP заголовками
     в читабельном виде"""
    return JsonResponse(
        json_object,
        status=status,
        safe= not isinstance(json, list),
        json_dumps_params=JSON_DUMPS_PARAMS
    )

def error_response(exception):
    res = {'errorMessage': str(exception),
          'traceback': traceback.format_exc()
          }
    return ret(res, status=400)


def base_view(fn):
    """Декоратор для всех вьюх"""
    @functools.wraps(fn)
    def inner(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return fn(request, *args, **kwargs)
        except Exception as exception:
            return error_response(exception)
        
    return inner

