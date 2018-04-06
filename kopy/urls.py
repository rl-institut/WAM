"""kopy URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from kopy.settings import DEBUG, WAM_APPS
from testing.test_highcharts import HighchartsTestView

urlpatterns = [
    url(
        r'^$',
        RedirectView.as_view(
            pattern_name='stemp:select',
            permanent=False)
        ),
    url(r'^admin/', admin.site.urls),
]

for app_name in WAM_APPS:
    app_url = url(
        r'^{}/'.format(app_name),
        include(app_name + '.urls', namespace=app_name)
    )
    urlpatterns.append(app_url)

if DEBUG:
    urlpatterns.append(url(r'^test/', HighchartsTestView.as_view()))
