
from django.apps import AppConfig

from wam import settings


class UserSessionsConfig(AppConfig):
    name = 'user_sessions'

    def ready(self):
        """This function is executed right after project settings"""

        # Initialize user sessions:
        from user_sessions.sessions import SessionData
        settings.SESSION_DATA = SessionData()
