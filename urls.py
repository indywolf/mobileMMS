from django.conf.urls import patterns, url
from login.views import login
from register.views import register
from home.views import home
from find.views import find

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/?', login),
    url(r'^register/?', register),
    url(r'^find/?', find),

    # Examples:
    url(r'^$', home)
    # url(r'^mobileMMS/', include('mobileMMS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)