from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^', include('web.urls', namespace='web')),
    url(r'^search/', include('haystack.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
