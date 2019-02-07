import os
from django.views.generic import ListView
from wam.settings import BASE_DIR

from meta.models import Assumption


class AppListView(ListView):
    """Lists all entries of an app-related model

    Model can be filtered by app_name attribute. If base template is given
    within specified app this template is extended. The base template
    is assumed to be located at
    <WAM_base_dir>/<app_name>/templates/<app_name>/base.html .

    If base template is not found, base template from meta app is taken.

    Usage:
        # in urls.py:

        from meta.models import AppListView, Source

        urlpatterns = [
            ...
            path('sources', AppListView.as_view(
                model=Source, app_name='stemp')
            ),
            ...
        ]

    Notes
    -----
    * Template can be named <model_name>_list.html to override default template
    * Models are defined in :mod:`~.meta.models`
    * The template displays all items of a model in a table, each row has a
    unique id
    """
    default_template_name = 'meta/app_list.html'
    app_name = None
    ordering = ['category__name']

    def __init__(self, *args, **kwargs):
        super(AppListView, self).__init__(*args, **kwargs)
        if self.app_name is not None:
            self.queryset = self.model.objects.filter(
                app_name=self.app_name)
        else:
            self.queryset = self.model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AppListView, self).get_context_data(
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

        # Highlight specific id:
        highlight_id = self.request.GET.get(self.model._meta.model_name, None)
        if (
                highlight_id is not None and
                context['object_list'].filter(pk=highlight_id).exists()
        ):
            context['highlight'] = str(highlight_id)

        # Highlight category:
        category_id = self.request.GET.get('category', None)
        if (
                category_id is not None and
                context['object_list'].filter(
                    category__pk=category_id).exists()
        ):
            context['category'] = str(category_id)

        return context

    def get_template_names(self):
        names = super(AppListView, self).get_template_names()
        return names + [self.default_template_name]


class AssumptionsView(AppListView):
    source_url = None
    model = Assumption

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssumptionsView, self).get_context_data(
            object_list=object_list, **kwargs)
        if self.source_url is not None:
            context['source_url'] = self.source_url
        else:
            if self.app_name is not None:
                context['source_url'] = self.app_name + ':sources'
            else:
                context['source_url'] = 'sources'
        return context
