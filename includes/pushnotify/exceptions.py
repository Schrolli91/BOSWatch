#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Jeffrey Goettsch and other contributors.
#
# This file is part of py-pushnotify.
#
# py-pushnotify is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# py-pushnotify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with py-pushnotify.  If not, see <http://www.gnu.org/licenses/>.

"""Module for exceptions.

"""


class PushNotifyError(Exception):
    """Base exception for all pushnotify errors.

    Args:
        args[0]: A string containing a message.
        args[1]: An integer containing an error.

    """

    def __init__(self, *args):

        super(PushNotifyError, self).__init__()
        self.args = [arg for arg in args]


class ApiKeyError(PushNotifyError):
    """Raised when a provided API key is invalid

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """

    pass


class FormatError(PushNotifyError):
    """Raised when a request is not in the expected format.

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """

    pass


class PermissionDenied(PushNotifyError):
    """Raised when a request had not been approved.

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """

    pass


class ProviderKeyError(PushNotifyError):
    """Raised when a provided Provider key is invalid.

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """
    pass


class RateLimitExceeded(PushNotifyError):
    """Raised when too many requests are submitted in too small a time
    frame.

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """

    pass


class ServerError(PushNotifyError):
    """Raised when the notification server experiences an internal error.

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """

    pass


class UnknownError(PushNotifyError):
    """Raised when the notification server returns an unknown error.

    Args:
        args[0]: A string containing a message from the server.
        args[1]: An integer containing an error code from the server.

    """

    pass


class UnrecognizedResponseError(PushNotifyError):
    """Raised when the notification server returns an unrecognized
    response.

    Args:
        args[0]: A string containing the response from the server.
        args[1]: -1.

    """

    pass


if __name__ == '__main__':
    pass
