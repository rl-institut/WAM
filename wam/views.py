import os
import importlib
from collections import defaultdict
from configobj import ConfigObj

from django.views.generic import TemplateView
from django.shortcuts import render_to_response

from wam.settings import WAM_APPS, BASE_DIR
from utils.constants import AppInfo, AppCategory


class ContactView(TemplateView):
    template_name = "contact.html"


class PrivacyView(TemplateView):
    template_name = "privacy_statement.html"


class ImpressumView(TemplateView):
    template_name = "impressum.html"


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        app_infos = defaultdict(list)
        for app in WAM_APPS:
            for app_info in self.get_app_infos(app):
                app_infos[app_info.category].append(app_info)
        app_infos.default_factory = None
        context["app_infos"] = app_infos
        return context

    @staticmethod
    def get_app_infos(app_name):
        # First, try to get app infos from app_settings.app_infos() function:
        try:
            app_settings = importlib.import_module(f"{app_name}.app_settings")
        except ImportError:
            pass
        else:
            if hasattr(app_settings, "app_infos"):
                return app_settings.app_infos()

        # Second, try to read app.cfg:
        app_config = ConfigObj(os.path.join(BASE_DIR, app_name, "app.cfg"))
        if len(app_config) > 0:
            return [
                AppInfo(
                    category=AppCategory(app_config["category"]),
                    name=app_config["name"],
                    url=f"{app_name}:index",
                    closed=app_config.get("closed", False),
                    icon=app_config["icon"],
                )
            ]
        # Third, return generic app info:
        return [
            AppInfo(category=AppCategory.App, name=app_name, url=f"{app_name}:index")
        ]

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)


def handler404(
    request, exception, template_name="error.html"
):  # pylint: disable=unused-argument
    """A custom 404 page"""
    context = {"err_text": "Die Seite wurde leider nicht gefunden"}
    response = render_to_response(template_name, context=context)
    response.status_code = 404
    return response


def handler500(request, template_name="error.html"):  # pylint: disable=unused-argument
    """A custom 500 page"""
    context = {"err_text": "Es ist ein Server-Fehler aufgetreten"}
    response = render_to_response(template_name, context=context)
    response.status_code = 500
    return response
