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
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^movie/(?P<id>[0-9a-zA-Z]+)/$', views.getMovie),
    url(r'^trending/$', views.getMovieTrending),
    url(r'^genres-profile/(?P<id>[0-9a-zA-Z]+)/$', views.getGenresMoviesByUserId),
    url(r'^get-top-genres-profile/(?P<id>[0-9a-zA-Z]+)/$', views.getTopGenresProfileByUserId),
    url(r'^login/(?P<userId>[0-9a-zA-Z]+)/(?P<password>[0-9a-zA-Z]+)/$', views.login),
]