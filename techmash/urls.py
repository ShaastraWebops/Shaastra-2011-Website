from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *
#from techmash.views import hello, current_datetime,hours_ahead, register,profile,addphonebook,viewbook,upload_file1
from main_test.techmash.views import register,profile,upload_file1,seephotos,selectimages,mashphotos
from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
             (r'^accounts/login/$',  login),
             (r'^accounts/logout/$', logout),
             (r'^accounts/register/$', register),
             (r'^accounts/profile/$', profile),
             (r'^upload/$', upload_file1),
             (r'^upload_file1/$', upload_file1),
             (r'^seephotos/$', seephotos),
             (r'^selectimages/$', selectimages),
             (r'^mashphotos/$', mashphotos),
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

