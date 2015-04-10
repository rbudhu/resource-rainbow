from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^', include('web.urls', namespace='web')),
    url(r'^admin/', include(admin.site.urls)),
]
