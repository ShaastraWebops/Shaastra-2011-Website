# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from django.contrib import admin
import django.contrib.auth.views
admin.autodiscover()

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"

urlpatterns = patterns('',
    url(r'^$', 'main_test.myshaastra.views.home'),
    url(r'^edit/profile/$', 'main_test.myshaastra.views.edit_profile'),
    url(r'^edit/password/$', 'main_test.myshaastra.views.edit_password'),
    url(r'^teams/create/$', 'main_test.myshaastra.views.create_team'),
    url(r'^teams/join/$', 'main_test.myshaastra.views.join_team'),
)
