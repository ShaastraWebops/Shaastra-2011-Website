# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.simple import *
from main_test.misc.util import *
handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"
#This is the broad outline of the urls as in the userportal with 
#few changes,If we want to change the url names later it
#wouldn't be too much of a problem.
urlpatterns = patterns('main_test.registration.views',
      (r'^register/instructions/?$','register_instructions') ,
      (r'^register/instructions/([a-z]+)/?$','template_to_view'),
      
#      (r'^register/events/?$' , 'register_events' ),
      (r'^register/user/?$', 'register_user'),
      (r'^register/team/?$', 'register_team'),
      (r'^register/coord/?$', 'register_coord'),
      (r'^register/college/?$', 'register_college'),
      (r'^register/mass/?$', 'mass_register'),
#      (r'^register/user/college/?$' , 'get_college' ),
      (r'^register/user/college/?$' , 'register_college' ),
#      (r'^register/convert/$', 'user_to_coord'),
      (r'^register/activate/(?P<a_key>[\w]+)/?$', 'activate'),

      (r'^profile/?$', 'profile'),
      (r'^profile/view/(?P<u_name>.*)/?$', 'super_profile'),
      (r'^profile/edit/?$', 'edit_profile'),
      (r'^profile/edit/(?P<u_id>.*)/?$', 'edit_profile'),

      (r'^teams/?$', 'view_teams'),
      (r'^teams/view/(?P<t_name>[a-zA-Z0-9_.-]*)/?$', 'view_teams'),
#      (r'^teams/view/(?P<t_name>[a-zA-Z0-9_]*)/(?P<e_name>.*)/$', 'register_team_events'),
      (r'^teams/join/?$', 'join_team'),
      (r'^teams/manage/?$', 'manage_teams'),
      (r'^teams/manage/(?P<t_name>[a-zA-Z0-9_.-]*)/?$', 'manage_teams'),
      (r'^teams/manage/(?P<t_name>[a-zA-Z0-9_.-]*)/changepwd/?$', 'change_password'),
      (r'^teams/remove/(?P<t_name>[a-zA-Z0-9_.-]+)/(?P<u_name>[a-zA-Z0-9_.-]+)/?$', 'remove_team_member'),
)

