
from django.urls import path

from wam.admin import wam_admin_site

from user_sessions import views


app_name = 'user_sessions'

url_patterns = []

admin_url_patterns = [
    path(
        'sessions/manage',
        wam_admin_site.admin_view(views.ManageView.as_view()),
        name='manage'
    ),
]
