import logging

from django.shortcuts import render

from wam.settings import SESSION_DATA
from utils.shortcuts import get_app_from_request


def check_session_method(func):
    """
    Checks and returns session if it exists

    This method is for class-based views
    """

    def func_wrapper(self, request, *args, **kwargs):
        try:
            session = SESSION_DATA.get_session(request)
        except KeyError:
            log_session_error(request)
            return render(request, "stemp/session_not_found.html")
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
            log_session_error(request)
            return render(request, "stemp/session_not_found.html")
        return func(request, session=session, *args, **kwargs)

    return func_wrapper


def log_session_error(request):
    app = get_app_from_request(request)
    err_msg = (
        f'Session error for app "{app}":\n'
        f"Session-Key: {request.session.session_key}\n"
        f"Current session data:\n"
        + "\n".join([f"{k}: {str(v)}" for k, v in SESSION_DATA.sessions[app].items()])
    )
    logging.error(err_msg)
