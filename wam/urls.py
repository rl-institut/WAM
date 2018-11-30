"""wam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

from wam.admin import wam_admin_site
from wam.settings import WAM_APPS
from wam.views import IndexView


urlpatterns = [
    path('', IndexView.as_view()),
    path('admin/', wam_admin_site.urls),
    path('accounts/login/', LoginView.as_view(template_name='login.html')),
    path('access_denied/', TemplateView.as_view(
        template_name='access_denied.html'), name='access_denied')
]

try:
    urlpatterns.append(re_path(r'^markdownx/', include('markdownx.urls')))
except ImportError:
    pass

for app_name in WAM_APPS:
    app_url = path(
        '{}/'.format(app_name),
        include(app_name + '.urls', namespace=app_name)
    )
    urlpatterns.append(app_url)
