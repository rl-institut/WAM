
import importlib

from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from wam import settings


class WamAdminSite(AdminSite):
    def get_urls(self):
        admin_urls = super(WamAdminSite, self).get_urls()
        for app in settings.WAM_APPS:
            urls_module = importlib.import_module(f'{app}.urls')
            try:
                admin_urls.extend(urls_module.admin_url_patterns)
            except AttributeError:
                pass
        return admin_urls


wam_admin_site = WamAdminSite()
wam_admin_site.register(User, UserAdmin)
wam_admin_site.register(Group, GroupAdmin)
