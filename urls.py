from django.conf.urls.defaults import *
#from upload.views import upload_file

from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"
defaultdict = { 'groupName': 'example' }
#testing
urlpatterns = patterns('',
    
    # (r'^upload/$', 'upload_file'),
    # Examples:
    # url(r'^$', 'main_test.views.home', name='home'),
    # url(r'^main_test/', include('main_test.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^home/$', 'main_test.misc.util.render_home' ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^events/', include ('main_test.events.urls')),
    url(r'^forum/', include('main_test.forum.urls')),  
    url(r'^techmash/', include ('main_test.techmash.urls')),  
    url(r'^myshaastra/', include('main_test.myshaastra.urls')),
    url(r'^search/$', 'main_test.search.views.custom_search'),
    #url(r'^sitemap\.xml$', 'main_test.events.views.sitemap'),
    url(r'^', include ('main_test.users.urls')),
    url(r'^confluence/', 'main_test.confluence.views.rsvp'),
    url(r'^(?P<static_name>.*)/$', 'main_test.events.views.render_static'),
    (r'^community/', include('sphene.community.urls'), defaultdict),
    (r'^board/', include('sphene.sphboard.urls'), defaultdict),
    (r'^wiki/', include('sphene.sphwiki.urls'), defaultdict),
    (r'^static/sphene/(.*)$', 'django.views.static.serve', {'document_root': '/home/swaroop/main_test/sct-0.6/communitytools/static/sphene' }),	
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url':'home/'}),
)
#Checking if this is reflected.
