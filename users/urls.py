# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from django.contrib import admin
import django.contrib.auth.views
admin.autodiscover()

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"

urlpatterns = patterns('django.contrib.auth.views',
(r'^password_reset/$', 'password_reset'),
(r'^password_reset/done/$', 'password_reset_done'),
(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm'),
(r'^reset/done/$', 'password_reset_complete'),
)

urlpatterns = patterns('main_test.users.views',  
        
      (r'^register/user/?$', 'user_registration'),
      (r'^register/college/?$', 'college_registration'),
      (r'^myshaastra/$', 'myshaastra'),
      (r'^register/activate/(?P<a_key>[\w]+)/?$', 'activate'),
      (r'^login/?$', 'login'),
      (r'^logout/?$', 'logout'),

)   



