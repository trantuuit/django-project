from django.conf.urls import include, url
from rest_framework import routers
from snippets import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^user/$', views.userList),
    url(r'^user/(?P<id>[0-9a-zA-Z]+)/$', views.user_detail),
    url(r'^collaborative-filtering/(?P<id>[0-9a-zA-Z]+)/$', views.getMovieFromCollaborativeFilteringByUserId),
    url(r'^similarity/(?P<id>[0-9a-zA-Z]+)/$', views.getMovieFromSimilarityByMovieId),
    url(r'^last-action/(?P<id>[0-9a-zA-Z]+)/$', views.getMovieFromLastActionByUserId),
    url(r'^what-is-popular/$', views.getMovieFromWhatIsPupular),
    url(r'^login/$', views.login),
    url(r'^api-token-auth/', obtain_jwt_token)
]