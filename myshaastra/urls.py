# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from django.contrib import admin
import django.contrib.auth.views
admin.autodiscover()

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"

urlpatterns = patterns('',
    url(r'^$', 'main_test.myshaastra.views.home'),
    url(r'^edit/profile/$', 'main_test.users.views.edit_profile'),
    url(r'^teams/$', 'main_test.myshaastra.views.team_home'),
    url(r'^teams/create/$', 'main_test.myshaastra.views.create_team'),
    url(r'^teams/details/$', 'main_test.myshaastra.views.add_member'),
    url(r'^teams/change_leader/$', 'main_test.myshaastra.views.change_team_leader'),
    url(r'^teams/drop_out/$', 'main_test.myshaastra.views.drop_out'),
    url(r'^teams/remove_member/$', 'main_test.myshaastra.views.remove_member'),
)
