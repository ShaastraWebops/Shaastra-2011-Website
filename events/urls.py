from django.conf.urls.defaults import *
from main_test.events.views import *

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"

urlpatterns = patterns('main_test.events.views',
      (r'^/$', 'coordslogin'),
      (r'^login/$', 'coordslogin'),
      (r'^logout/$', 'logout'),
      (r'^dashboard/$', 'dashboard'),
      (r'^dashboard/add_tab/$', 'add_quick_tab'),
      (r'^dashboard/delete_file/$', 'remove_file'),
      (r'^dashboard/edit_tab/$', 'edit_tab_content'),
      (r'^dashboard/delete_tab/$', 'remove_quick_tab'),
      (r'^(?P<event_name>.*)/$', 'show_quick_tab'),
      (r'^dashboard/edit_event/$', 'edit_event'),
)

