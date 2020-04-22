from django.shortcuts import redirect


def redirect_with_get_parameters(url, **parameters):
    assert isinstance(parameters, dict)
    response = redirect(url)
    response["Location"] += "?" + "&".join(
        [str(key) + "=" + str(value) for key, value in parameters.items()]
    )
    return response


def get_app_from_request(request):
    try:
        return request.path.split("/")[1]
    except AttributeError:
        raise AttributeError("Current app could not be found")
