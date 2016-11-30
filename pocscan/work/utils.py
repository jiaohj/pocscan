# -*- coding: utf-8 -*-
import json
from functools import wraps

try:
    from django.core.serializers.json import DjangoJSONEncoder
except ImportError:
    from django.core.serializers.json import DateTimeAwareJSONEncoder as DjangoJSONEncoder


def jsonify(func=None, jsonp=None, content_type='application/json'):
    """Make view's response into JSON format"""

    from django.http import HttpResponse

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            rv = func(request, *args, **kwargs)

            if isinstance(rv, HttpResponse):
                return rv

            content = json.dumps(rv, cls=DjangoJSONEncoder,
                                 indent=None if request.is_ajax() else 2)
            if jsonp and request.GET.get(jsonp, default=None):
                fn = request.GET.get(jsonp)
                content = "%s(%s)" % (fn, content)
            response = HttpResponse(content=content, content_type=content_type)
            response['Cache-Control'] = 'no-cache'

            return response

        return wrapper

    if func is None:
        return decorator
    else:
        return decorator(func)
