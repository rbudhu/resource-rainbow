from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from web import views

urlpatterns = [
    url(r'^$', views.StatusCreate.as_view(), name='status-create'),
    url(r'^js/resource_rainbow/urls.js', views.URLView.as_view(), name='urls'),
    url(r'^login/?$', login, {'template_name': 'web/login.html'},
        name='login'),
    url(r'^logout/?$', logout, {'next_page': '/login'},
        name='logout'),
    url(r'^dispatch/?$', views.DispatchView.as_view()),
    url(r'^search/?$', login_required(views.UserSearch()), name='user-search'),
    url(r'^skill/search/?$', views.SkillSearch.as_view(),
        name='skill-search'),
    url(r'^user/create/?$', views.UserCreate.as_view(),
        name='user-create'),
    url(r'^user/update/(?P<pk>[0-9]+)/?$', views.UserUpdate.as_view(),
        name='user-update'),
    url(r'^user/(?P<pk>[0-9]+)/?$', views.UserDetail.as_view(),
        name='user-detail'),
    url(r'^workgroup/create/?$', views.WorkGroupCreate.as_view(),
        name='workgroup-create'),
    url(r'^workgroups/?$', views.WorkGroupList.as_view(),
        name='workgroup-list'),
    url(r'^workgroup/(?P<pk>[0-9]+)/?$', views.WorkGroupDetail.as_view(),
        name='workgroup-detail'),
    url(r'^workgroup/user/add/?$', views.WorkGroupUserAdd.as_view(),
        name='workgroup-user-add'),
    url(r'^workgroup/user/remove/?$', views.WorkGroupUserRemove.as_view(),
        name='workgroup-user-remove'),
]
