# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

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
      (r'^view_feedback/?$', 'main_test.users.views.view_feedback'),
      (r'^password_change/$', 'django.contrib.auth.views.password_change'),
      (r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),
      (r'^myshaastra/forgot_password/$', 'main_test.users.views.forgot_password'),
      (r'^myshaastra/forgot_password/done/$', direct_to_template, { 'template' : 'users/forgot_password_done.html', } ),
      (r'^myshaastra/reset_password/$', 'main_test.users.views.reset_password'),
      (r'^myshaastra/reset_password/done/$', direct_to_template, { 'template' : 'users/reset_password_done.html', } ),
      (r'^myshaastra/edit_profile/$','main_test.users.views.edit_profile'),
      (r'^spons/$', 'main_test.users.views.spons_dashboard'),

)   



