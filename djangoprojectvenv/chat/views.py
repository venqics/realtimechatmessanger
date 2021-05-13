from django.shortcuts import render, redirect
from chat.models import PrivateChatRoom, RoomChatMessage

from django.conf import settings


def private_chat_room_view(request, *args, **kwargs):
	
    user = request.user
	# Redirect them if not authenticate
    if not user.is_authenticated:
		return redirect("login")

    context = {}
    return render(request, "chat/room.html", context)