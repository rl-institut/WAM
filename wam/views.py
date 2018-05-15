
from django.views.generic import TemplateView
from wam.settings import WAM_APPS


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        context['apps'] = {app: app + ':index' for app in WAM_APPS}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)
