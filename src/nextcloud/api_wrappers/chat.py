# -*- coding: utf-8 -*-
from typing import Optional

from nextcloud.base import WithRequester, ConversationType


# https://nextcloud-talk.readthedocs.io/en/latest/chat/


class Chat(WithRequester):
    API_URL = "/ocs/v2.php/apps/spreed/api/v1/chat"
    SUCCESS_CODE = 200

    def add_one_to_one_conversation(self, invite):
        """
        Create new one-to-one conversation

        :param str invite: Conversation partners (group/circle)
        """
        data = {"roomType": ConversationType.ONE_TO_ONE.value, "invite": invite}

        return self.requester.post(data=data)

    def add_group_conversation(self, conversation_name, invite=None, source="groups"):
        """
        Create new group conversation

        :param str conversation_name: Name of new conservation
        :param str invite: Conversation partners (group/circle)
        :param str source: groups/circles
        """
        data = {
            "roomType": ConversationType.GROUP.value,
            "invite": invite,
            "roomName": conversation_name,
            "source": source,
        }

        return self.requester.post(data=data)

    def add_public_conversation(self, conversation_name):
        """
        Create new public conversation

        :param str conversation_name: Name of new conservation
        """
        data = {
            "roomType": ConversationType.PUBLIC.value,
            "roomName": conversation_name,
        }

        return self.requester.post(data=data)

    def get_messages(
        self,
        conversation_id,
        look_into_future: int = 0,
        limit: int = 200,
        last_known_message_id: Optional[int] = None,
        timeout=30,
        set_read_marker=1,
        include_last_known=0,
    ):
        """
        Get all messages of a conversation

        :param str conversation_id: Conversation ID
        :param int look_into_future: Poll and wait for new message (1) or get history of a conversation (0)
        :param int limit: Number of chat messages to receive
        :param int last_known_message_id: Serves as an offset for the query
        :param int timeout: Number of seconds to wait for new messages (used only if look_into_future is 1)
        :param int set_read_marker: 1 to automatically set the read timer after fetching the messages, use 0 when your client calls Mark chat as read manually
        :return: Chat messages
        :rtype: list
        """

        assert look_into_future in [0, 1], "look_into_future must be 1 or 0."
        assert set_read_marker in [0, 1], "set_read_marker must be 1 or 0."
        assert include_last_known in [0, 1], "include_last_known must be 1 or 0."

        data = {
            "lookIntoFuture": look_into_future,
            "limit": limit,
            "setReadMarker": set_read_marker,
            "includeLastKnown": include_last_known,
        }

        if look_into_future == 1:
            data["timeout"] = timeout

        if last_known_message_id is not None:
            data["lastKnownMessageId"] = last_known_message_id

        return self.requester.get(conversation_id, data=data)

    def get_conversation(self, conversation_id):
        """
        Get single conversation

        :param str conversation_id: Conversation ID
        :return: Conversation
        :rtype: dict
        """

        return self.requester.get(conversation_id)

    def rename_conversation(self, conversation_id, conversation_name):
        """
        Rename a conversation

        :param str conversation_id: Conversation ID
        :param str conversation_name: Name of new conversation
        """

        data = {"roomName": conversation_name}

        return self.requester.put(conversation_id, data)

    def delete_conversation(self, conversation_id):
        """
        Delete a conversation

        :param str conversation_id:
        :return:
        """

        return self.requester.delete(conversation_id)

    def make_conversation_public(self, conversation_id):
        """
        Make a conversation public

        :param str conversation_id: Conversation ID
        :return:
        """

        return self.requester.post("{}/public".format(conversation_id))

    def make_conversation_private(self, conversation_id):
        """
        Make a conversation private (group conversation)

        :param str conversation_id: Conversation ID
        :return:
        """

        return self.requester.delete("{}/public".format(conversation_id))

    def set_read_only_conversation(self, conversation_id, state):
        """
        Set read-only state of a conversation

        :param str conversation_id: Conversation ID
        :param bool state: False (read-write) / True (read-only)
        :return:
        """

        data = {"state": int(state)}

        return self.requester.put("{}/read-only".format(conversation_id), data)

    def set_conversation_password(self, conversation_id, password):
        """
        Set password for a conversation

        :param str conversation_id: Conversation ID
        :param str password: Conversation password
        :return:
        """

        data = {"password": password}

        return self.requester.put("{}/password".format(conversation_id), data)

    def add_conversation_to_favorites(self, conversation_id):
        """
        Add conversation to favorites

        :param str conversation_id: Conversation ID
        :return:
        """

        return self.requester.post("{}/favorite".format(conversation_id))

    def remove_conversation_from_favorites(self, conversation_id):
        """
        Remove conversation from favorites

        :param str conversation_id: Conversation ID
        :return:
        """

        return self.requester.delete("{}/favorite".format(conversation_id))

    def set_notification_level(self, conversation_id, level):
        """
        Set password for a conversation

        :param str conversation_id: Conversation ID
        :param int level: Level
        :return:
        """

        data = {"level": level}

        return self.requester.post("{}/notify".format(conversation_id), data)
