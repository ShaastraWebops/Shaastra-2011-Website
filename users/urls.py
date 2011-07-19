# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from django.contrib import admin
import django.contrib.auth.views
admin.autodiscover()

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"


urlpatterns = patterns('',  
        
      (r'^register/user/?$', 'main_test.users.views.user_registration'),
      (r'^edit/user/?$', 'main_test.users.views.edit_profile'),
      (r'^register/college/?$', 'main_test.users.views.college_registration'),
      (r'^register/activate/(?P<a_key>[\w]+)/?$', 'main_test.users.views.activate'),
      (r'^login/?$', 'main_test.users.views.login'),
      (r'^logout/?$', 'main_test.users.views.logout'),
      (r'^feedback/?$', 'main_test.users.views.feedback'),
      (r'^password_change/$', 'django.contrib.auth.views.password_change'),
      (r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),
      

)   



