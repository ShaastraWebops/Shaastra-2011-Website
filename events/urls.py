from django.conf.urls.defaults import *
from views import *

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"

urlpatterns = patterns('main_test.events.views',
      (r'^/$', 'coordslogin'),
      (r'^login/$', 'coordslogin'),
      (r'^logout/$', 'logout'),
      (r'^dashboard/$', 'dashboard'),
      (r'^dashboard/add_tab/$', 'add_quick_tab'),
      (r'^dashboard/delete_file/$', 'remove_file'),
      (r'^dashboard/add_file/$', 'add_file'),
      (r'^dashboard/edit_tab/$', 'edit_tab_content'),
      (r'^dashboard/delete_tab/$', 'remove_quick_tab'),
      (r'^(?P<event_name>.*)/$', 'show_quick_tab'),
      (r'^dashboard/edit_event/$', 'edit_event'),
)

