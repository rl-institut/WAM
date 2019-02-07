import os
from django.views.generic import ListView
from meta import models
from wam.settings import BASE_DIR


class AppListView(ListView):
    """Lists all entries of an app-related model

    Model can be filtered by app_name attribute. If base template is given
    within specified app, SourceView extends this template. The base template
    is assumed to be located at
    <WAM_base_dir>/<app_name>/templates/<app_name>/base.html .

    If base template is not found, base template from meta app is taken.
    """
    app_name = None
    ordering = ['category__name']
    model = None

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


class SourcesView(AppListView):
    """Lists all sources grouped by category.

    Usage:
        # in urls.py:

        from meta.models import SourceView

        urlpatterns = [
            ...
            path('sources', SourcesView.as_view(app_name='stemp')),
            ...
        ]

    Notes
    -----
    * Models are defined in :mod:`~.meta.models`
    * The sources template displays all sources in a table, each row has a
    unique id

    """
    template_name = 'meta/sources.html'
    model = models.Source

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SourcesView, self).get_context_data(
            object_list=object_list, **kwargs)

        return context


class AssumptionsView(AppListView):
    """Lists all assumptions grouped by category.

    Usage:
        # in urls.py:

        from meta.models import AssumptionsView

        urlpatterns = [
            ...
            path('assumptions', AssumptionsView.as_view(app_name='stemp')),
            ...
        ]

    Notes
    -----
    * Models are defined in :mod:`~.meta.models`
    * The assumptions template displays all assumptions in a table,
    each row has a unique id

    """
    template_name = 'meta/assumptions.html'
    model = models.Assumption
