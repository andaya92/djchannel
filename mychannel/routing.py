from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
	re_path(r'^ws/mychannel/room/(?P<room_name>\w+)/$', consumers.ChatConsumer),
	re_path(r'^ws/mychannel/camshow/(?P<room_name>\w+)/$', consumers.CamShow),
	re_path('ws/mychannel/servercam/', consumers.CamConsumer),

]