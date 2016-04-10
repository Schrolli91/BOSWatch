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

"""Module for sending push notifications to Android devices that have
Notify My Android installed. See www.notifymyandroid.com/ for more
information.

"""


import warnings
try:
    from xml.etree import cElementTree
    ElementTree = cElementTree
except ImportError:
    from xml.etree import ElementTree

from includes.pushnotify import abstract
from includes.pushnotify import exceptions


PUBLIC_API_URL = u'https://www.notifymyandroid.com/publicapi'
VERIFY_URL = u'/'.join([PUBLIC_API_URL, 'verify'])
NOTIFY_URL = u'/'.join([PUBLIC_API_URL, 'notify'])

DESC_LIMIT = 10000


class Client(abstract.AbstractClient):
    """Client for sending push notificiations to Android devices with
    the Notify My Android (NMA) application installed.

    Member Vars:
        developerkey: A string containing a valid developer key for the
            NMA application.
        application: A string containing the name of the application on
            behalf of whom the NMA client will be sending messages.
        apikeys: A dictionary where the keys are strings containing
            valid user API keys, and the values are lists of strings,
            each containing a valid user device key. Device keys are not
            used by this client.

    """

    def __init__(self, developerkey='', application=''):
        """Initialize the Notify My Android client.

        Args:
            developerkey: A string containing a valid developer key for
                the NMA application.
            application: A string containing the name of the application
                on behalf of whom the NMA client will be sending
                messages.

        """

        super(self.__class__, self).__init__(developerkey, application)

        self._type = 'nma'
        self._urls = {'notify': NOTIFY_URL, 'verify': VERIFY_URL}

    def _parse_response(self, response, verify=False):

        xmlresp = response.text
        root = ElementTree.fromstring(xmlresp)

        self._last['type'] = root[0].tag.lower()
        self._last['code'] = root[0].attrib['code']

        if self._last['type'] == 'success':
            self._last['message'] = None
            self._last['remaining'] = root[0].attrib['remaining']
            self._last['resettimer'] = root[0].attrib['resettimer']
        elif self._last['type'] == 'error':
            self._last['message'] = root[0].text
            self._last['remaining'] = None
            self._last['resettimer'] = None

            if (not verify or
                    (self._last['code'] != '400' and
                        self._last['code'] != '401')):
                self._raise_exception()
        else:
            raise exceptions.UnrecognizedResponseError(xmlresp, -1)

        return root

    def _raise_exception(self):

        if self._last['code'] == '400':
            raise exceptions.FormatError(self._last['message'],
                                         int(self._last['code']))
        elif self._last['code'] == '401':
            raise exceptions.ApiKeyError(self._last['message'],
                                         int(self._last['code']))
        elif self._last['code'] == '402':
            raise exceptions.RateLimitExceeded(self._last['message'],
                                               int(self._last['code']))
        elif self._last['code'] == '500':
            raise exceptions.ServerError(self._last['message'],
                                         int(self._last['code']))
        else:
            raise exceptions.UnknownError(self._last['message'],
                                          int(self._last['code']))

    def notify(self, description, event, split=True, kwargs=None):
        """Send a notification to each user's apikey in self.apikeys.

        Args:
            description: A string of up to DESC_LIMIT characters
                containing the main notification text.
            event: A string of up to 1000 characters containing a
                subject or brief description of the event.
            split: A boolean indicating whether to split long
                descriptions among multiple notifications (True) or to
                possibly raise an exception (False). (default True)
            kwargs: A dictionary with any of the following strings as
                    keys:
                priority: An integer between -2 and 2, indicating the
                    priority of the notification. -2 is the lowest, 2 is
                    the highest, and 0 is normal.
                url: A string of up to 2000 characters containing a URL
                    to attach to the notification.
                content_type: A string containing "text/html" (without
                    the quotes) that then allows some basic HTML to be
                    used while displaying the notification.
                (default: None)

        Raises:
            pushnotify.exceptions.ApiKeyError
            pushnotify.exceptions.FormatError
            pushnotify.exceptions.RateLimitExceeded
            pushnotify.exceptions.ServerError
            pushnotify.exceptions.UnknownError
            pushnotify.exceptions.UnrecognizedResponseError

        Returns:
            True.

        """

        def send_notify(description, event, kwargs):
            data = {'apikey': ','.join(self.apikeys),
                    'application': self.application,
                    'event': event,
                    'description': description}

            if self.developerkey:
                data['developerkey'] = self.developerkey

            if kwargs:
                data.update(kwargs)

            response = self._post(self._urls['notify'], data)
            self._parse_response(response)

        if not self.apikeys:
            self.logger.warn('notify called with no users set')
            return

        if split:
            while description:
                this_desc = description[0:DESC_LIMIT]
                description = description[DESC_LIMIT:]
                send_notify(this_desc, event, kwargs)
        else:
            send_notify(description, event, kwargs)

        return True

    def verify(self, apikey):
        """This method is deprecated. Use verify_user instead.

        """

        msg = 'The verify method is deprecated. User verify_user instead.'
        self.logger.warn(msg)
        warnings.warn(msg, DeprecationWarning)

        return self.verify_user(apikey)

    def verify_user(self, apikey):
        """Verify a user's API key.

        Args:
            apikey: A string of 48 characters containing a user's API
                key.

        Raises:
            pushnotify.exceptions.RateLimitExceeded
            pushnotify.exceptions.ServerError
            pushnotify.exceptions.UnknownError
            pushnotify.exceptions.UnrecognizedResponseError

        Returns:
            A boolean containing True if the user's API key is valid,
            and False if it is not.

        """

        data = {'apikey': apikey}

        if self.developerkey:
            data['developerkey'] = self.developerkey

        response = self._get(self._urls['verify'], data)
        self._parse_response(response, True)

        return self._last['code'] == '200'

if __name__ == '__main__':
    pass
