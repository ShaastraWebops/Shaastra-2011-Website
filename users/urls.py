# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from django.contrib import admin

admin.autodiscover()

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"

urlpatterns = patterns('main_test.users.views',  

      (r'^register/user/?$', 'user_registration'),
      (r'^register/college/?$', 'college_registration'),
      (r'^myshaastra/$', 'myshaastra'),

)   



