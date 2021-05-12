from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from django.contrib.auth import get_user_model

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
		


	async def disconnect(self, code):
		"""
		Called when the WebSocket closes for any reason.
		"""
		# leave the room
		print("PublicChatConsumer: disconnect")
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
			elif command == "get_room_chat_messages":
				await self.display_progress_bar(True)
				room = await get_room_or_error(content['room_id'])
				payload = await get_room_chat_messages(room, content['page_number'])
				if payload != None:
					payload = json.loads(payload)
					await self.send_messages_payload(payload['messages'], payload['new_page_number'])
				else:
					raise ClientError(204,"Something went wrong retrieving the chatroom messages.")
				await self.display_progress_bar(False)
		except ClientError as e:
			await self.display_progress_bar(False)
			await self.handle_client_error(e)

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