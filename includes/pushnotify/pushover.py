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

"""Module for sending push notificiations to Android and iOS devices
that have Pushover installed. See https://pushover.net/ for more
information.

"""


import time

from includes.pushnotify import abstract
from includes.pushnotify import exceptions


PUBLIC_API_URL = u'https://api.pushover.net/1'
VERIFY_URL = u'/'.join([PUBLIC_API_URL, u'users/validate.json'])
NOTIFY_URL = u'/'.join([PUBLIC_API_URL, u'messages.json'])
SOUND_URL = u'/'.join([PUBLIC_API_URL, u'sounds.json'])

DESC_LIMIT = 512


class Client(abstract.AbstractClient):
    """Client for sending push notifications to Android and iOS devices
    with the Pushover application installed.

    Member Vars:
        developerkey: A string containing a valid token for the Pushover
            application.
        application: A string containing the name of the application on
            behalf of whom the Pushover client will be sending messages.
            Not used by this client.
        apikeys: A dictionary where the keys are strings containing
            valid user identifier, and the values are lists of strings,
            each containing a valid device identifier.

    """

    def __init__(self, developerkey, application=''):
        """Initialize the Pushover client.

        Args:
            developerkey: A string containing a valid token for the
                Pushover application.
            application: A string containing the name of the application
                on behalf of whom the Pushover client will be sending
                messages. Not used by this client. (default: '')

        """

        super(self.__class__, self).__init__(developerkey, application)

        self._type = 'pushover'
        self._urls = {'notify': NOTIFY_URL,
                      'verify': VERIFY_URL,
                      'sounds': SOUND_URL}

    def _parse_response(self, stream, verify=False):

        response = stream.json()
        self.logger.info('received response: {0}'.format(response))

        self._last['code'] = stream.status_code
        self._last['device'] = response.get('device', None)
        self._last['errors'] = response.get('errors', None)
        self._last['status'] = response.get('status', None)
        self._last['token'] = response.get('token', None)
        self._last['user'] = response.get('user', None)
        self._last['sounds'] = response.get('sounds', None)
        self._last['receipt'] = response.get('receipt', None)

        return self._last['status']

    def _raise_exception(self):

        msg = ''
        if self._last['errors']:
            messages = []
            for error in self._last['errors']:
                messages.append(error)
            msg = '; '.join(messages)

        if self._last['device'] and 'invalid' in self._last['device']:
            raise exceptions.ApiKeyError('device invalid', self._last['code'])

        elif self._last['token'] and 'invalid' in self._last['token']:
            raise exceptions.ApiKeyError('token invalid', self._last['code'])

        elif self._last['user'] and 'invalid' in self._last['user']:
            raise exceptions.ApiKeyError('user invalid', self._last['code'])

        elif self._last['code'] == 429:
            # TODO: what is actually returned when the rate limit is hit?

            msg = 'too many messages sent this month' if not msg else msg
            raise exceptions.RateLimitExceeded(msg, self._last['code'])

        elif self._last['code'] >= 500 and self._last['code'] <= 599:
            raise exceptions.ServerError(msg, self._last['code'])

        elif self._last['errors']:
            raise exceptions.FormatError(msg, self._last['code'])

        else:
            raise exceptions.UnrecognizedResponseError(msg, self._last['code'])

    def notify(self, description, event, split=True, kwargs=None):
        """Send a notification to each user/device combintation in
        self.apikeys.

        As of 2012-09-18, this is not returning a 4xx status code as
        per the Pushover API docs, but instead chopping the delivered
        messages off at 512 characters.

        Args:
            description: A string of up to DESC_LIMIT characters
                containing the notification text.
            event: A string of up to 100 characters containing a
                subject or brief description of the event.
            split: A boolean indicating whether to split long
                descriptions among multiple notifications (True) or to
                possibly raise an exception (False). (default True)
            kwargs: A dictionary with any of the following strings as
                    keys:
                priority: An integer between -1 and 2, indicating low (-1),
                    normal (0), high (1), or emergency (2) priority.
                    (see: https://pushover.net/api#priority)
                retry: An integer specifying how often, in seconds, to resend
                    the notification until acknowledged. Must be 30 or
                    greater. Requires a priority value of 2.
                expire: An integer specifying when, in seconds, to stop
                    resending the notification. Must be 86400 or less.
                    Requires a priority value of 2.
                url: A string of up to 500 characters containing a URL
                    to attach to the notification.
                url_title: A string of up to 50 characters containing a
                    title to give the attached URL.
                sound: A string containing a valid sound returned from
                    get_sounds().
                (default: None)

        Raises:
            pushnotify.exceptions.ApiKeyError
            pushnotify.exceptions.FormatError
            pushnotify.exceptions.RateLimitExceeded
            pushnotify.exceptions.ServerError
            pushnotify.exceptions.UnrecognizedResponseError

        Returns:
            A string containing the last receipt received, if priority
            was sent to 2, otherwise True.

        """

        def send_notify(desc_list, event, kwargs, apikey, device_key=''):
            all_successful = True

            for description in desc_list:
                data = {'token': self.developerkey,
                        'user': apikey,
                        'title': event,
                        'message': description,
                        'timestamp': int(time.time())}

                if device_key:
                    data['device'] = device_key

                if kwargs:
                    data.update(kwargs)

                response = self._post(self._urls['notify'], data)
                this_successful = self._parse_response(response)

                all_successful = all_successful and this_successful

            return all_successful

        if not self.apikeys:
            self.logger.warn('notify called with no users set')
            return

        desc_list = []
        if split:
            while description:
                desc_list.append(description[0:DESC_LIMIT])
                description = description[DESC_LIMIT:]
        else:
            desc_list = [description]

        # Here we match the behavior of Notify My Android and Prowl:
        # raise a single exception if and only if every notification
        # fails

        all_ok = True

        for apikey, device_keys in self.apikeys.items():
            if not device_keys:
                this_ok = send_notify(desc_list, event, kwargs, apikey)
            else:
                for device_key in device_keys:
                    this_ok = send_notify(
                        desc_list, event, kwargs, apikey, device_key)

            all_ok = all_ok and this_ok

        if not all_ok:
            self._raise_exception()

        return self._last['receipt'] if self._last['receipt'] else True

    def verify_user(self, apikey):
        """Verify a user identifier.

        Args:
            apikey: A string containing a user identifer.

        Returns:
            A boolean containing True if apikey is valid, and
            False if it is not.

        """

        data = {'token': self.developerkey, 'user': apikey}

        response = self._post(self._urls['verify'], data)

        self._parse_response(response, True)

        return self._last['status']

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

        data = {'token': self.developerkey, 'user': apikey,
                'device': device_key}

        response = self._post(self._urls['verify'], data)

        self._parse_response(response, True)

        if self._last['user'] and 'invalid' in self._last['user'].lower():
            self._raise_exception()

        return self._last['status']

    def get_sounds(self):
        """ Retrieve available sounds list.

        Returns:
            A dictionary with each key being the actual sound parameter to store for the user
            and send to Pushover, with its value describing the sound.
        """
        response = self._get(self._urls['sounds'],
                             {'token': self.developerkey})
        self._parse_response(response, True)
        return self._last['sounds']

if __name__ == '__main__':
    pass
