# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"

urlpatterns = patterns('main_test.events.views',
      (r'^/$', 'coordslogin'),
)
"""   
      (r'^login/$', 'login'),
      (r'^login/forgot/$', 'forgot_password'),
      (r'^login/forgot/(?P<u_name>[a-zA-Z0-9_.-]+)/(?P<new_pass>[\w]+)/?$', 'reset_password'),
      (r'^logout/$', 'logout'),
      (r'^check/$','check'),
      (r'^deadlines/$','deadlines'),
       
      (r'^registered/$','registered'),
           
      (r'^register/instructions/?$','register_instructions') ,
      (r'^register/instructions/([a-z]+)/?$','template_to_view'),
       
      (r'^register/user/?$', 'user_registration'),
       
      (r'^register/team/?$', 'register_team'),
      (r'^register/coord/?$', 'register_coord'),
      (r'^register/college/?$', 'register_college'),
      (r'^register/mass/?$', 'mass_register'),
      (r'^register/user/college/?$' , 'register_college' ),
      (r'^register/activate/(?P<a_key>[\w]+)/?$', 'activate'),
      (r'^profile/?$', 'profile'),
      (r'^profile/view/(?P<u_name>.*)/?$', 'super_profile'),
      (r'^profile/edit/?$', 'edit_profile'),
      (r'^profile/edit/(?P<u_id>.*)/?$', 'edit_profile'),
      (r'^teams/?$', 'view_teams'),
      (r'^teams/view/(?P<t_name>[a-zA-Z0-9_.-]*)/?$', 'view_teams'),
      (r'^teams/join/?$', 'join_team'),
      (r'^teams/manage/?$', 'manage_teams'),
      (r'^teams/manage/(?P<t_name>[a-zA-Z0-9_.-]*)/?$', 'manage_teams'),
      (r'^teams/manage/(?P<t_name>[a-zA-Z0-9_.-]*)/changepwd/?$', 'change_password'),
      (r'^teams/remove/(?P<t_name>[a-zA-Z0-9_.-]+)/(?P<u_name>[a-zA-Z0-9_.-]+)/?$', 'remove_team_member'),
    """



