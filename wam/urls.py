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
from django.urls import path, include, re_path
from django.contrib import admin

from wam.settings import WAM_APPS
from wam.views import IndexView


urlpatterns = [
    path('', IndexView.as_view()),
    path('admin/', admin.site.urls),
    re_path(r'^markdownx/', include('markdownx.urls')),
]

for app_name in WAM_APPS:
    app_url = path(
        '{}/'.format(app_name),
        include(app_name + '.urls', namespace=app_name)
    )
    urlpatterns.append(app_url)
