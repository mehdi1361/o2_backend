__author__ = 'mousavi'
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from o2_api import views
from django.conf.urls import include
urlpatterns = [
    url(r'^game/$', views.GameList.as_view()),
    url(r'^game/(?P<pk>[0-9]+)/$', views.GameDetail.as_view()),
    url(r'^game/register', views.game_score_register),
    url(r'^game/leaderboard', views.game_leader_board),
    url(r'^game/golden', views.golden_tournament),
    url(r'^game/package', views.buy_package),
    url(r'^game/use_gem', views.use_gem),

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^users/register', views.CreateUserView.as_view()),
    url(r'^users/device', views.device_validation),
    url(r'^users/send_verify_code', views.send_device_verified),
    url(r'^users/send_verify', views.send_verify),
    url(r'^users/verification', views.confirm_verification),
]
urlpatterns = format_suffix_patterns(urlpatterns)

# urlpatterns = [
#     url(r'^users/$', views.user_list),
#     url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)
