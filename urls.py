from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

handler404 = 'signmeup.views.page_not_found'

urlpatterns = patterns(
    '',
    (r'^$', 'signmeup.views.home'),
    (r'^topic/(?P<topic_id>[A-Za-z0-9\-]+)/signup', 'signmeup.views.signup_topic'),
    (r'^topic/(?P<topic_id>[A-Za-z0-9\-]+)/list$', 'signmeup.views.view_topic_signups'),
    (r'^topic/(?P<topic_id>[A-Za-z0-9\-]+)$', 'signmeup.views.view_topic'),
    (r'^topics', 'signmeup.views.all_topics'),
    (r'^new_topic', 'signmeup.views.define_topic'),
    #(r'^admin/$', 'signmeup.views.admin.home'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
