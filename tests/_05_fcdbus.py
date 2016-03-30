#!/usr/bin/python
# -*- coding: utf-8 -*-
# vi:ts=4 sw=4 sts=4

# Copyright (C) 2015 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the licence, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# Authors: Alberto Ruiz <aruiz@redhat.com>
#          Oliver Gutiérrez <ogutierrez@redhat.com>

# Python imports
import os
import sys

import dbus

PYTHONPATH = os.path.join(os.environ['TOPSRCDIR'], 'admin')
sys.path.append(PYTHONPATH)

# Fleet commander imports
from fleetcommander import fcdbus


class MockLibVirtController(object):

    def __init__(self, data_path, username, hostname, mode, admin_hostname, admin_port):

        self.data_dir = os.path.abspath(data_path)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.public_key_file = os.path.join(self.data_dir, 'id_rsa.pub')

        with open(self.public_key_file, 'w') as fd:
            fd.write('PUBLIC_KEY')
            fd.close()

    def list_domains(self):
        return [{'uuid': 'e2e3ad2a-7c2d-45d9-b7bc-fefb33925a81', 'name': 'fedora-unkno'}]

    def session_start(self, uuid):
        return ('someuuid', 0, 'tunnel_pid')

    def session_stop(self, uuid, tunnel_pid):
        pass


# Mock libvirt controller
fcdbus.libvirtcontroller.LibVirtController = MockLibVirtController


class TestFleetCommanderDbusService(fcdbus.FleetCommanderDbusService):

    def __init__(self):
        test_directory = os.environ['FC_TEST_DIRECTORY']

        args = {
            'data_dir': test_directory,
            'state_dir': test_directory,
            'database_path': os.path.join(test_directory, 'database.db'),
        }

        super(TestFleetCommanderDbusService, self).__init__(args)

if __name__ == '__main__':
    svc = TestFleetCommanderDbusService()
    svc.run(sessionbus=True)