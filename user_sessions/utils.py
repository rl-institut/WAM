from django.shortcuts import render

from wam.settings import SESSION_DATA


def check_session_method(func):
    """
    Checks and returns session if it exists

    This method is for class-based views
    """
    def func_wrapper(self, request, *args, **kwargs):
        try:
            session = SESSION_DATA.get_session(request)
        except KeyError:
            return render(request, 'stemp/session_not_found.html')
        return func(self, request, session=session, *args, **kwargs)
    return func_wrapper


def check_session(func):
    """
        Checks and returns session if it exists

        This function is for function-based views
        """
    def func_wrapper(request, *args, **kwargs):
        try:
            session = SESSION_DATA.get_session(request)
        except KeyError:
            return render(request, 'stemp/session_not_found.html')
        return func(request, session=session, *args, **kwargs)
    return func_wrapper
