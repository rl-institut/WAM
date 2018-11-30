import os
from django.views.generic import ListView
from meta import models
from wam.settings import BASE_DIR


class SourcesView(ListView):
    """
    Lists all sources grouped by source category

    Sources can be filtered by app_name attribute. If base template is given
    within specified app, SourceView extends this template. The base template
    is assumed to be located at
    <WAM_base_dir>/<app_name>/templates/<app_name>/base.html .

    if base template is not found, base template from meta app is taken.

    Usage:
        # in urls.py:

        from meta.models import SourceView

        urlpatterns = [
            ...
            path('sources', SourcesView.as_view(app_name='stemp')),
            ...
        ]
    """
    template_name = 'meta/sources.html'
    app_name = None
    ordering = ['category__name']

    def __init__(self, *args, **kwargs):
        super(SourcesView, self).__init__(*args, **kwargs)
        if self.app_name is not None:
            self.queryset = models.Source.objects.filter(
                app_name=self.app_name)
        else:
            self.queryset = models.Source.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SourcesView, self).get_context_data(
            object_list=object_list, **kwargs)

        # Try to load base.html template from app:
        base_template = 'meta/base.html'
        if self.app_name is not None:
            base_template_file = os.path.join(
                BASE_DIR,
                self.app_name,
                'templates',
                self.app_name,
                'base.html'
            )
            if os.path.exists(base_template_file):
                base_template = self.app_name + '/base.html'
        context['base_template'] = base_template
        return context
