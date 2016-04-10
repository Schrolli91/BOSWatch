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

import logging

from includes.pushnotify._version import __version__
import includes.pushnotify.nma
import includes.pushnotify.prowl
import includes.pushnotify.pushover


logger = logging.getLogger(__package__)


def get_client(type_, developerkey='', application=''):
    """Get a pushnotify client of the specified type.

    Args:
        type_: A string containing the type of client to get. Valid
            types are 'nma,' 'prowl,', and 'pushover,' for Notify My
            Android, Prowl, and Pushover clients, respectively.
        developerkey: A string containing a valid developer key for the
            given type_ of client.
        application: A string containing the name of the application on
            behalf of whom the client will be sending messages.

    Returns:
        An nma.Client, prowl.Client, or pushover.Client.

    """

    type_ = type_.lower()

    if type_ == 'nma':
        return nma.Client(developerkey, application)
    elif type_ == 'prowl':
        return prowl.Client(developerkey, application)
    elif type_ == 'pushover':
        return pushover.Client(developerkey, application)


if __name__ == '__main__':
    pass
