from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.contrib.auth import get_user_model

from django.contrib.humanize.templatetags.humanize import naturaltime, naturalday
from django.utils import timezone
from datetime import datetime
from chat.utils import calculate_timestamp
from djangoprojectvenv.public_chat.models import PublicChatRoom

User = get_user_model()

MSG_TYPE_MESSAGE = 0  # For standard messages


# Example taken from:
# https://github.com/andrewgodwin/channels-examples/blob/master/multichat/chat/consumers.py

class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code, message):
        super().__init__(code)
        self.code = code
        if message:
        	self.message = message




class PublicChatConsumer(AsyncJsonWebsocketConsumer):

	async def connect(self):
		"""
		Called when the websocket is handshaking as part of initial connection.
		"""
		print("PublicChatConsumer: connect: " + str(self.scope["user"]))
		# let everyone connect. But limit read/write to authenticated users
		await self.accept()
		self.room_id = None


	async def disconnect(self, code):
		"""
		Called when the WebSocket closes for any reason.
		"""
		# leave the room
		print("PublicChatConsumer: disconnect")
		try:
			if self.room_id != None:
				await self.leave_room(self.room_id)
		except Exception:
			pass



	async def receive_json(self, content):
		"""
		Called when we get a text frame. Channels will JSON-decode the payload
		for us and pass it as the first argument.
		"""
		# Messages will have a "command" key we can switch on
		command = content.get("command", None)
		print("PublicChatConsumer: receive_json: " + str(command))
		try:
			if command == "send":
				if len(content["message"].lstrip()) != 0:
					await self.send_room(content["room_id"], content["message"])
					# raise ClientError(422,"You can't send an empty message.")
			elif command == "join":
				# Make them join the room
				await self.join_room(content["room"])
			elif command == "leave":
				# Leave the room
				await self.leave_room(content["room"])
			
		except ClientError as e:
			await self.display_progress_bar(False)
			await self.handle_client_error(e)


	async def chat_message(self, event):
		"""
		Called when someone has messaged our chat.
		"""
		# Send a message down to the client
		print("PublicChatConsumer: chat_message from user #" + str(event["user_id"]))
		timestamp = calculate_timestamp(timezone.now())
		await self.send_json(
			{
				"msg_type": MSG_TYPE_MESSAGE,
				"profile_image": event["profile_image"],
				"username": event["username"],
				"user_id": event["user_id"],
				"message": event["message"],
				"natural_timestamp": timestamp,
			},
		)

	async def join_room(self, room_id):
		"""
		Called by receive_json when someone sent a join command.
		"""
		print("PublicChatConsumer: join_room")
		is_auth = is_authenticated(self.scope["user"])
		try:
			room = await get_room_or_error(room_id)
		except ClientError as e:
			await self.handle_client_error(e)

		# Add user to "users" list for room
		if is_auth:
			await connect_user(room, self.scope["user"])

		# Store that we're in the room
		self.room_id = room.id

		# Add them to the group so they get room messages
		await self.channel_layer.group_add(
			room.group_name,
			self.channel_name,
		)

		# Instruct their client to finish opening the room
		await self.send_json({
			"join": str(room.id)
		})

		# send the new user count to the room
		num_connected_users = get_num_connected_users(room)
		await self.channel_layer.group_send(
			room.group_name,
			{
				"type": "connected.user.count",
				"connected_user_count": num_connected_users,
			}
		)


	async def leave_room(self, room_id):
		"""
		Called by receive_json when someone sent a leave command.
		"""
		print("PublicChatConsumer: leave_room")
		is_auth = is_authenticated(self.scope["user"])
		room = await get_room_or_error(room_id)

		# Remove user from "users" list
		if is_auth:
			await disconnect_user(room, self.scope["user"])

		# Remove that we're in the room
		self.room_id = None
		# Remove them from the group so they no longer get room messages
		await self.channel_layer.group_discard(
			room.group_name,
			self.channel_name,
		)

		# send the new user count to the room
		num_connected_users = get_num_connected_users(room)
		await self.channel_layer.group_send(
		room.group_name,
			{
				"type": "connected.user.count",
				"connected_user_count": num_connected_users,
			}
		)

	async def handle_client_error(self, e):
		"""
		Called when a ClientError is raised.
		Sends error data to UI.
		"""
		errorData = {}
		errorData['error'] = e.code
		if e.message:
			errorData['message'] = e.message
			await self.send_json(errorData)
		return

	

	



def is_authenticated(user):
	if user.is_authenticated:
		return True
	return False

@database_sync_to_async
def connect_user(room, user):
    return room.connect_user(user)

@database_sync_to_async
def disconnect_user(room, user):
    return room.disconnect_user(user)

@database_sync_to_async
def get_room_or_error(room_id):
	"""
	Tries to fetch a room for the user
	"""
	try:
		room = PublicChatRoom.objects.get(pk=room_id)
	except PublicChatRoom.DoesNotExist:
		raise ClientError("ROOM_INVALID", "Invalid room.")
	return room

