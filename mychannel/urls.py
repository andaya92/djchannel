from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'mychannel'

urlpatterns = [
    url(r'^$', views.Index.as_view(), name="index"),
    url(r'^room/(?P<room_name>[^/]+)/$', views.Room.as_view(), name="room"),
    url(r'^camshow/(?P<room_name>[^/]+)/$', views.Room.as_view(), name="camroom"),
    url('servercam/', views.ServerCam.as_view(), name="server_cam"),

]