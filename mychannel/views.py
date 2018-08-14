from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
import json
# Create your views here.
import logging
console = logging.getLogger('__name__')

class Index(TemplateView):
	def get(self, request):
		return render(request, 'mychannel/index.html')

class Room(TemplateView):
	def get(self,request,room_name):
		return render(request, 'mychannel/room.html',{
			'room_name_json' : mark_safe(json.dumps(room_name))
			})
		
class CamRoom(TemplateView):
	def get(self,request,room_name):
		return render(request, 'mychannel/camshow.html',{
			'room_name_json' : mark_safe(json.dumps(room_name))
			})

class ServerCam(TemplateView):
	console.error("ServerRoom")
	def get(self, request):
		return render(request, 'mychannel/servercam.html')