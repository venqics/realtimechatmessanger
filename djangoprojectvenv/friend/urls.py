from django.urls import path

from .views import send_friend_request, friend_requests,accept_friend_request, remove_friend, decline_friend_request

app_name = 'friend'

urlpatterns = [ 
     path('friend_request/', send_friend_request, name='friend-request'),
     path('friend_request/<user_id>/', friend_requests, name='friend-requests'),
     path('friend_remove/', remove_friend, name='remove-friend'),
     path('friend_request_decline/<friend_request_id>/', decline_friend_request, name='friend-request-decline'),
]

