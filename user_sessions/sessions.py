from collections import defaultdict
from utils.shortcuts import get_app_from_request


class SessionData(object):
    def __init__(self):
        self.sessions = defaultdict(dict)

    def start_session(self, request, session_obj):
        if request.session.session_key is None:
            request.session.create()
        app = get_app_from_request(request)
        if request.session.session_key not in self.sessions[app]:
            self.sessions[app][request.session.session_key] = session_obj()

    def get_session(self, request):
        app = get_app_from_request(request)
        user_session = self.sessions[app].get(
            request.session.session_key, None)
        if user_session is None:
            raise KeyError('Session not found')
        else:
            return user_session
