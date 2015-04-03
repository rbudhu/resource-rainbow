from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^account/', include('account.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
