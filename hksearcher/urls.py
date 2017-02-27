from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

import hksearcher
from web import views

admin.autodiscover()

urlpatterns = [url(r'^$', views.home, name='home'),
               url(r'^motors$', views.loadMotors, name='home'),
               url(r'^loadMotors$', views.loadMotors, name='load'),
               url(r'^motorDesc$', views.motorDesc, name='load'),
               url(r'^batteries$', views.loadBatteries, name='home'),
               url(r'^loadBatteries$', views.loadBatteries, name='load'),
               url(r'^batDesc$', views.batDesc, name='load'),
               # url(r'^hksearcher/', include('hksearcher.foo.urls')),

               # Uncomment the admin/doc line below to enable admin documentation:
               # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

               # Uncomment the next line to enable the admin:
               url(r'^admin/', admin.site.urls),
               url(r'^media/(?P<path>.*)$', serve, {'document_root': hksearcher.settings.MEDIA_ROOT})
               ]
