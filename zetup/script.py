#!python

# zetup.py
#
# Zimmermann's Python package setup.
#
# Copyright (C) 2014 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# zetup.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# zetup.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with zetup.py. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import sys
import os
from textwrap import dedent
from argparse import ArgumentParser
from subprocess import call
import distutils.command

from path import path as Path

import zetup
import zetup.commands
from zetup.commands import ZetupCommandError


COMMANDS = zetup.commands.__all__

EXTERNAL_COMMANDS = []

COMMANDS += distutils.command.__all__
COMMANDS += zetup.Zetup.COMMANDS
COMMANDS += EXTERNAL_COMMANDS

ap = ArgumentParser()
ap.add_argument(
  'cmd', choices=COMMANDS,
  help="command",
  )

args = ap.parse_args()


def run():
    exit_status = 0 # exit status of this script
    try:
        cmdfunc = getattr(zetup, args.cmd)
    except AttributeError:
        if args.cmd in EXTERNAL_COMMANDS:
            exit_status = call([args.cmd])
        else:
            zetup = zetup.Zetup()
            if args.cmd in zetup.COMMANDS:
                try:
                    exit_status = getattr(zetup, args.cmd)()
                except ZetupCommandError as e:
                    print("Error: %s" % e, file=sys.stderr)
                    exit_status = 1
                else:
                    try: # return value can be more than just a status number
                        exit_status = exit_status.status
                    except AttributeError:
                        pass
            else: # ==> standard setup command
                zetup(subprocess=True)
    else:
        exit_status = cmdfunc()

    sys.exit(exit_status or 0)


if __name__ == '__main__':
    run()