from django.conf.urls.defaults import *
#from upload.views import upload_file

from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

handler404 = "main_test.misc.util.not_found"
handler500 = "main_test.misc.util.server_error"

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
	
	#temporary
	url(r'^event-details/$', direct_to_template, { 'template' : 'event-details.html', } )
	url(r'^event_categories/$', direct_to_template, { 'template' : 'event_categories_2.html', } )
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url':'home/'}),
)
#Checking if this is reflected.
