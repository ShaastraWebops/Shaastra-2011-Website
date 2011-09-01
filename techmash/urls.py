
from django.conf.urls.defaults import *
from views import *
from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',

             (r'^profile/$', profile),
             (r'^upload/$', upload),
             (r'^mashphotos/$', mashphotos),
             (r'^delete/(?P<image_title>.*)/$', deleteimage),
             (r'^(?P<username>.*)/showprofile/$', profile),
#            (r'^stockphoto/', include('stockphoto.urls')),
#            (r'^admin/', include('admin.site.urls')),


# Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable thpythone admin:
   # url(r'^admin/', include(admin.site.urls)),
)

