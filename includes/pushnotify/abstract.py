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

"""Module for abstract class.

"""

import logging
import requests


class AbstractClient(object):
    """Abstract client for sending push notifications. Inherit from this
    class but don't call it directly.

    Member Vars:
        developerkey: A string containing a valid developer key for the
            client's application.
        application: A string containing the name of the application on
            behalf of whom the client will be sending messages.
        apikeys: A dictionary where the keys are strings containing
            valid user API keys, and the values are lists of strings,
            each containing a valid user device key.

    """

    def __init__(self, developerkey='', application=''):
        """Initialize the client.

        Args:
            developerkey: A string containing a valid developer key for
                the client's application.
            application: A string containing the name of the application
                on behalf of whom the client will be sending messages.

        """

        self.logger = logging.getLogger('{0}.{1}'.format(
            self.__module__, self.__class__.__name__))

        if not application:
            application = 'pushnotify'

        self.developerkey = developerkey
        self.application = application
        self.apikeys = {}

        self._browser = requests.Session()
        self._last = {}
        self._urls = {'notify': '', 'verify': ''}

    def _get(self, url, data):

        self.logger.debug('_get requesting url: {0}'.format(url))

        return self._browser.get(url, params=data)

    def _post(self, url, data):

        self.logger.debug('_post sending data: {0}'.format(data))
        self.logger.debug('_post sending to url: {0}'.format(url))

        return self._browser.post(url, data=data)

    def add_key(self, apikey, device_key=''):
        """Add the given key to self.apikeys.

        Args:
            apikey: A string containing a valid user's API key for the
                client's application.
            device_key: A string containing a valid device key to go
                along with the API key. (default: '')
        """

        if apikey not in self.apikeys:
            self.apikeys[apikey] = []

        if device_key and device_key not in self.apikeys[apikey]:
            self.apikeys[apikey].append(device_key)

    def del_key(self, apikey, device_key=''):
        """Delete the given API key or device key from self.apikeys.

        If device_key is not set, delete apikey and all of its device
        keys. Otherwise only delete the device key.

        Args:
            apikey: A string containing a valid user's API key that is
                in self.apikeys.
            device_key: A string containing a valid device key that is
                in self.apikeys[apikey]. (default: '')

        """

        if device_key:
            self.apikeys[apikey] = [value for value in self.apikeys[apikey]
                                    if value != device_key]
        else:
            del(self.apikeys[apikey])

    def notify(self, description, event, split=True, kwargs=None):
        """Send a notification to each user/device combination in
        self.apikeys.

        Args:
            description: A string containing the main notification text.
                The maximum length varies by application. See each
                client's documentation for details.
            event: A string containing a subject or brief description of
                the event. The maximum length varies by application. See
                each client's documentation for details.
            split: A boolean indicating whether to split long
                descriptions among multiple notifications (True) or to
                raise an exception if it is too long (False).
                (default True)
            kwargs: A dictionary for application specific options. See
                each client's documentation for details.
                (default: None)

        Raises:
            pushnotify.exceptions.ApiKeyError
            pushnotify.exceptions.FormatError
            pushnotify.exceptions.RateLimitExceeded
            pushnotify.exceptions.ServerError
            pushnotify.exceptions.UnknownError
            pushnotify.exceptions.UnrecognizedResponseError

        """

        raise NotImplementedError

    def retrieve_apikey(self, reg_token):

        raise NotImplementedError

    def retrieve_token(self):

        raise NotImplementedError

    def verify_device(self, apikey, device_key):
        """Verify a device identifier for the user given by apikey.

        Args:
            apikey: A string containing a user identifer.
            device_key: A string containing a device identifier.

        Raises:
            pushnotify.exceptions.ApiKeyError

        Returns:
            A boolean containing True if device_key is valid for
            apikey, and False if it is not.

        """

        raise NotImplementedError

    def verify_user(self, apikey):
        """Verify a user's API key.

        Args:
            apikey: A string containing a user's API key.

        Raises:
            pushnotify.exceptions.RateLimitExceeded
            pushnotify.exceptions.ServerError
            pushnotify.exceptions.UnknownError
            pushnotify.exceptions.UnrecognizedResponseError

        Returns:
            A boolean containing True if the user's API key is valid,
            and False if it is not.

        """

        raise NotImplementedError

    def get_sounds(self):
        """ Retrieve available sounds list.

        Returns:
            A dictionary with each key being the actual sound parameter to store for the user
            and send back with notify request, with its value describing the sound.
        """
        raise NotImplementedError
