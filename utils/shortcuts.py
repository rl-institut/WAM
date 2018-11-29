
from django.shortcuts import redirect


def redirect_with_get_parameters(url, **parameters):
    assert isinstance(parameters, dict)
    response = redirect(url)
    response['Location'] += '?' + '&'.join(
        [str(key) + '=' + str(value) for key, value in parameters.items()])
    return response
