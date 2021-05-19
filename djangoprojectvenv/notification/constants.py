DEFAULT_NOTIFICATION_PAGE_SIZE = 10

"""
"General" notifications include:
	1. FriendRequest
	2. FriendList
"""


GENERAL_MSG_TYPE_NOTIFICATIONS_PAYLOAD = 0  # New 'general' notifications data payload incoming
GENERAL_MSG_TYPE_UPDATED_NOTIFICATION = 5  # Update a notification that has been altered (Ex: Accept/decline a friend request)
GENERAL_MSG_TYPE_PAGINATION_EXHAUSTED = 1  # No more 'general' notifications to retrieve
GENERAL_MSG_TYPE_NOTIFICATIONS_REFRESH_PAYLOAD = 2  # Retrieved all 'general' notifications newer than the oldest visible on screen
GENERAL_MSG_TYPE_GET_NEW_GENERAL_NOTIFICATIONS = 3  # Get any new notifications
GENERAL_MSG_TYPE_GET_UNREAD_NOTIFICATIONS_COUNT = 4  # Send the number of unread "general" notifications to the template