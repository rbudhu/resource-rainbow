from django.conf.urls import include, url
from django.contrib.auth.views import login, logout
from web import views

urlpatterns = [
    url(r'^$', views.StatusCreate.as_view(),
        name='status-create'),
    url(r'^search/?$',  views.UserSearch(), name='user-search'),
    url(r'^login/?$', login, {'template_name': 'web/login.html'},
        name='login'),
    url(r'^logout/?$', logout, {'next_page': '/login'},
        name='logout'),
    url(r'^create/?$', views.UserCreate.as_view(),
        name='user-create'),
    url(r'^update/(?P<pk>[0-9]+)/?$', views.UserUpdate.as_view(),
        name='user-update'),
    url(r'^dispatch/?$', views.DispatchView.as_view()),
    url(r'^workgroup/create/?$', views.WorkGroupCreate.as_view(),
        name='workgroup-create'),
    url(r'^workgroups/?$', views.WorkGroupList.as_view(),
        name='workgroup-list'),
    url(r'^workgroup/(?P<pk>[0-9]+)/?$', views.WorkGroupDetail.as_view(),
        name='workgroup-detail'),
    url(r'^workgroup/user/add/?$', views.WorkGroupUserAdd.as_view(),
        name='workgroup-user-add'),
    ]
