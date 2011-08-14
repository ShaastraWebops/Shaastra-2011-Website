from django.conf.urls.defaults import *
from main_test.events.views import *

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"

urlpatterns = patterns('main_test.events.views',
      (r'^$', 'show_event_categories'),
      (r'^register/?$', 'register'),
      (r'^dashboard/$', 'dashboard'),
      (r'^dashboard/add_tab/$', 'add_quick_tab'),
      (r'^dashboard/add_questions_tab/$', 'add_questions_tab'),
      (r'^dashboard/add_question/$', 'add_question'),
      (r'^dashboard/delete_question/$', 'remove_question'),
      (r'^dashboard/edit_question/$', 'edit_questions'), 
      (r'^dashboard/delete_file/$', 'remove_file'),
      (r'^dashboard/add_choices/$', 'add_choices'),
      (r'^dashboard/delete_option/$', 'delete_option'),
      (r'^dashboard/add_file/$', 'add_file'),
      (r'^dashboard/edit_tab/$', 'edit_tab_content'),
      (r'^dashboard/delete_tab/$', 'remove_quick_tab'),
      (r'^dashboard/edit_event/$', 'edit_event'),
      (r'^UpdateSpons/$', 'UpdateSpons'),
      (r'^UpdateSponsPage/$', 'edit_spons'),
      (r'^images/(?P<event_name>.*)/$', 'event_image'),
      (r'^cores/$', 'cores_dashboard'),
      (r'^ImportantDates/$', 'EventCoresPage'),
      (r'^cores/EventCoresEditPage/$', 'EventCoresEditPage'), 
      
      #Add any more urls here
      (r'^(?P<event_name>.*)/$', 'show_quick_tab')     #This must always be the last url pattern to search for!!
      #!!End!!
)

