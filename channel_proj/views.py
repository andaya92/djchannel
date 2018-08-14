from django.views.generic import TemplateView
from django.shortcuts import render

class Index(TemplateView):
	def get(self, request):
		return render(request, 'channel_proj/index.html')