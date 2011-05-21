from django.conf.urls.defaults import *
from views import *

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"

urlpatterns = patterns('events.views',
      (r'^login/$', 'coordslogin'),
      (r'^login/$', 'coordslogin'),
      (r'^dashboard/$', 'dashboard'),
      (r'^dashboard/add_tab/$', 'add_quick_tab'),
      (r'^dashboard/edit_tab/$', 'edit_tab_content'),
      (r'^dashboard/delete_tab/$', 'remove_quick_tab'),
      (r'^(?P<event_name>.*)/$', 'show_quick_tab'),
)

