from stemp.user_data import UserSession


class SessionData(object):
    def __init__(self):
        self.sessions = {}

    def start_session(self, request):
        if request.session.session_key is None:
            request.session.create()
        if request.session.session_key not in self.sessions:
            self.sessions[request.session.session_key] = UserSession()

    def get_session(self, request):
        user_session = self.sessions.get(request.session.session_key, None)
        if user_session is None:
            raise KeyError('Session not found')
        else:
            return user_session
