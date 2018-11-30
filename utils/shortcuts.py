
import os
from django.shortcuts import redirect


def redirect_with_get_parameters(url, **parameters):
    assert isinstance(parameters, dict)
    response = redirect(url)
    response['Location'] += '?' + '&'.join(
        [str(key) + '=' + str(value) for key, value in parameters.items()])
    return response


def get_list_from_env(env_name):
    return list(filter(None, os.environ.get(env_name, "").split(',')))
