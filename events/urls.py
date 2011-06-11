from django.conf.urls.defaults import *
from main_test.events.views import *

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"

urlpatterns = patterns('main_test.events.views',
      (r'^$', 'show_event_categories'),
      (r'^login/$', 'coordslogin'),
      (r'^logout/$', 'logout'),
      (r'^dashboard/$', 'dashboard'),
      (r'^dashboard/add_tab/$', 'add_quick_tab'),
      (r'^dashboard/add_questions_tab/$', 'add_questions_tab'),
      (r'^dashboard/add_question/$', 'add_question'),
      (r'^dashboard/delete_question/$', 'remove_question'),
      (r'^dashboard/edit_question/$', 'edit_questions'), 
      (r'^dashboard/delete_file/$', 'remove_file'),
      (r'^dashboard/add_choices/$', 'add_choices'),
      (r'^dashboard/add_file/$', 'add_file'),
      (r'^dashboard/edit_tab/$', 'edit_tab_content'),
      (r'^dashboard/delete_tab/$', 'remove_quick_tab'),
      (r'^dashboard/edit_event/$', 'edit_event'),
      (r'^menus/$', 'show_menu_items'),
      #Add any more urls here
      (r'^(?P<event_name>.*)/$', 'show_quick_tab')     #This must always be the last url pattern to search for!!
      #!!End!!
)

