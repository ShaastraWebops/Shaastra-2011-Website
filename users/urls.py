# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"


urlpatterns = patterns('',  
        
      (r'^register/user/?$', 'main_test.users.views.user_registration'),
      (r'^register/college/?$', 'main_test.users.views.college_registration'),
      (r'^myshaastra/$', 'main_test.users.views.myshaastra'),
      (r'^register/activate/(?P<a_key>[\w]+)/?$', 'main_test.users.views.activate'),
      (r'^login/?$', 'main_test.users.views.login'),
      (r'^logout/?$', 'main_test.users.views.logout'),
      (r'^password_change/$', 'django.contrib.auth.views.password_change'),
      (r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),

)   



