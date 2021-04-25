from django.urls import path

from .views import send_friend_request, friend_requests

app_name = 'friend'

urlpatterns = [ 
     path('friend_request/', send_friend_request, name='friend-request'),
     path('friend_request/<user_id>/', friend_requests, name='friend-requests'),

]

