"""
URLConf for Django-Forum.

django-forum assumes that the forum application is living under
/forum/.

Usage in your base urls.py:
    (r'^forum/', include('forum.urls')),

"""

from django.conf.urls.defaults import *
from main_test.forum.models import Forum
from main_test.forum.feeds import RssForumFeed, AtomForumFeed
from main_test.forum.sitemap import ForumSitemap, ThreadSitemap, PostSitemap

feed_dict = {
    'rss' : RssForumFeed,
    'atom': AtomForumFeed
}

sitemap_dict = {
    'forums': ForumSitemap,
    'threads': ThreadSitemap,
    'posts': PostSitemap,
}

urlpatterns = patterns('',
    url(r'^$', 'main_test.forum.views.forums_list', name='forum_index'),
    
    url(r'^(?P<url>(rss|atom).*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feed_dict}),

    url(r'^thread/(?P<thread>[0-9]+)/$', 'main_test.forum.views.thread', name='forum_view_thread'),
    url(r'^thread/(?P<thread>[0-9]+)/reply/$', 'main_test.forum.views.reply', name='forum_reply_thread'),

    url(r'^subscriptions/$', 'main_test.forum.views.updatesubs', name='forum_subscriptions'),

    url(r'^(?P<slug>[-\w]+)/$', 'main_test.forum.views.forum', name='forum_thread_list'),
    url(r'^(?P<forum>[-\w]+)/new/$', 'main_test.forum.views.newthread', name='forum_new_thread'),

    url(r'^([-\w/]+/)(?P<forum>[-\w]+)/new/$', 'main_test.forum.views.newthread'),
    url(r'^([-\w/]+/)(?P<slug>[-\w]+)/$', 'main_test.forum.views.forum', name='forum_subforum_thread_list'),

    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemap_dict}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap_dict}),
)
