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
    url(r'^director-profile/(?P<id>[0-9a-zA-Z]+)/$', views.getDirectorMoviesByUserId),
    url(r'^get-top-director-profile/(?P<id>[0-9a-zA-Z]+)/$', views.getTopDirectorProfileByUserId),
    url(r'^writer-profile/(?P<id>[0-9a-zA-Z]+)/$', views.getWriterMoviesByUserId),
    url(r'^get-top-writer-profile/(?P<id>[0-9a-zA-Z]+)/$', views.getTopWriterProfileByUserId),
    url(r'^Drama/$', views.getDrama),
    url(r'^Action/$', views.getAction),
    url(r'^Animation/$', views.getAnimation),
    url(r'^Comedy/$', views.getComedy),
    url(r'^Sci-fi/$', views.getSci_Fi),
    url(r'^Documentary/$', views.getDocumentary),
    url(r'^Romance/$', views.getRomance),
    url(r'^Horror/$', views.getHorror),
    url(r'^Thriller/$', views.getThriller),
    url(r'^Adventure/$', views.getAdventure),
    url(r'^Fantasy/$', views.getFantasy),
    url(r'^register-survey/$', views.registerSurvey),
    url(r'^userevent/$', views.userevent),
    url(r'^last-like/(?P<id>[0-9a-zA-Z]+)/$', views.getLastLike),
    url(r'^get-top-last-watch/(?P<id>[0-9a-zA-Z]+)/$', views.getTopLastWatch),
    url(r'^get-last-watch/(?P<id>[0-9a-zA-Z]+)/$', views.getLastWatchByUserId)
]