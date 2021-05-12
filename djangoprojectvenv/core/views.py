from django.conf import settings
from django.shortcuts import render
def home_screen_view(request):
	context = {}
	context['debug_mode'] = settings.DEBUG
	context['room_id'] = "1"
	return render(request, "core/home.html", context)