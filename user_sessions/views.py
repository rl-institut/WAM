from django.views.generic import TemplateView

from wam.settings import SESSION_DATA


class ManageView(TemplateView):
    template_name = "user_sessions/manage.html"

    def get_context_data(self, **kwargs):
        return {"session_keys": SESSION_DATA.sessions.keys()}
