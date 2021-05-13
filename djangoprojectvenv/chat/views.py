from django.shortcuts import render, redirect
from chat.models import PrivateChatRoom, RoomChatMessage
from itertools import chain
from django.conf import settings


def private_chat_room_view(request, *args, **kwargs):
	
    user = request.user
	# Redirect them if not authenticate
    if not user.is_authenticated:
		return redirect("login")

    context = {}
    
    # 1. Find all the rooms this user is a part of 
    rooms1 = PrivateChatRoom.objects.filter(user1=user, is_active=True)
    rooms2 = PrivateChatRoom.objects.filter(user2=user, is_active=True)

	# 2. merge the lists
    rooms = list(chain(rooms1, rooms2))
    print(str(len(rooms)))
    
    """
    m_and_f:
		[{"message": "hey", "friend": "Mitch"}, {"message": "You there?", "friend": "Blake"},]
  	Where message = The most recent message
  """
    m_and_f = [] 
    for room in rooms:
		# Figure out which user is the "other user" (aka friend)
		  if room.user1 == user:
			  friend = room.user2
		  else:
			  friend = room.user1
		  m_and_f.append({
			  'message': "", # blank msg for now (since we have no messages)
			  'friend': friend
		  })
    context['m_and_f'] = m_and_f
    return render(request, "chat/room.html", context)