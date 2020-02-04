# -*- coding: utf-8 -*-
import enum


class WithRequester(object):

    API_URL = NotImplementedError

    def __init__(self, requester):
        self._requester = requester

    @property
    def requester(self):
        """ Get requester instance """
        # dynamically set API_URL for requester
        self._requester.API_URL = self.API_URL
        self._requester.SUCCESS_CODE = getattr(self, 'SUCCESS_CODE', None)
        return self._requester


class OCSCode(enum.IntEnum):
    OK = 100
    SERVER_ERROR = 996
    NOT_AUTHORIZED = 997
    NOT_FOUND = 998
    UNKNOWN_ERROR = 999


class ShareType(enum.IntEnum):
    USER = 0
    GROUP = 1
    PUBLIC_LINK = 3
    FEDERATED_CLOUD_SHARE = 6


class Permission(enum.IntEnum):
    """ Permission for Share have to be sum of selected permissions """
    READ = 1
    UPDATE = 2
    CREATE = 4
    DELETE = 8
    SHARE = 16
    ALL = 31


# Constants for Talk
# https://nextcloud-talk.readthedocs.io/en/latest/constants/


class ConversationType(enum.IntEnum):
    ONE_TO_ONE = 1
    GROUP = 2
    PUBLIC = 3
    CHANGELOG = 4


class ReadState(enum.IntEnum):
    READ_WRITE = 0
    READ_ONLY = 1


class ParticipantType(enum.IntEnum):
    OWNER = 1
    MODERATOR = 2
    USER = 3
    GUEST = 4
    PUBLIC_LINK = 5
    GUEST_MODERATOR = 6


class ParticipantInCallFlag(enum.IntEnum):
    DISCONNECTED = 0
    IN_CALL = 1
    PROVIDES_AUDIO = 2
    PROVIDES_VIDEO = 4


class ActorType(enum):
    GUESTS = "guests"
    USERS = "users"
    bots = "bots"


class WebinaryLobbyState(enum.IntEnum):
    NO_LOBBY = 0
    LOBBY = 1


QUOTA_UNLIMITED = -3


def datetime_to_expire_date(date):
    return date.strftime("%Y-%m-%d")
