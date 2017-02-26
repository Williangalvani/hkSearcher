from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'hksearcher.web.views.home', name='home'),
    url(r'^motors$', 'hksearcher.web.views.loadMotors', name='home'),
    url(r'^loadMotors$', 'hksearcher.web.views.loadMotors', name='load'),
    url(r'^motorDesc$', 'hksearcher.web.views.motorDesc', name='load'),
    url(r'^batteries$', 'hksearcher.web.views.loadBatteries', name='home'),
    url(r'^loadBatteries$', 'hksearcher.web.views.loadBatteries', name='load'),
    url(r'^batDesc$', 'hksearcher.web.views.batDesc', name='load'),
    # url(r'^hksearcher/', include('hksearcher.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
)
