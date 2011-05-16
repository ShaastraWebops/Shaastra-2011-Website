from django.conf.urls.defaults import *
#from upload.views import upload_file

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = "userportal.misc.util.not_found"
handler500 = "userportal.misc.util.server_error"

#testing
urlpatterns = patterns('',
    # (r'^upload/$', 'upload_file'),
    # Examples:
    # url(r'^$', 'main_test.views.home', name='home'),
    # url(r'^main_test/', include('main_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^main-test/admin/', include(admin.site.urls)),
     url(r'^main-test/events/', include ('main_test.events.urls')),
     url(r'^main-test/home/', include ('main_test.users.urls')),   
)

#Check
