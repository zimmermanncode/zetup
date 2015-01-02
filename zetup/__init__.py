# zetup.py
#
# Zimmermann's Python package setup.
#
# Copyright (C) 2014-2015 Stefan Zimmermann <zimmermann.code@gmail.com>
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

__all__ = ['Zetup', 'find_zetup_config']

import sys
import os
from inspect import ismodule

from .zetup import Zetup


def find_zetup_config(pkgname):
    zfg_pkgname = pkgname + '.zetup_config'
    try: # Already imported?
        return sys.modules[zfg_pkgname]
    except KeyError:
        pass
    try:
        return __import__(zfg_pkgname).zetup_config
    except ImportError:
        pass
    # ==> no .zetup_config subpackage
    # ==> assume package imported from source (repo)
    # ==> load setup config from package's parent path:
    mod = sys.modules[pkgname]
    path = os.path.dirname(os.path.dirname(os.path.realpath(mod.__file__)))
    return Zetup(path)


# Get zetup's own config:
zfg = find_zetup_config(__name__)

__distribution__ = zfg.DISTRIBUTION.find(__path__[0])
__description__ = zfg.DESCRIPTION

__version__ = zfg.VERSION

__requires__ = zfg.REQUIRES # .checked
## if ismodule(zfg): # if this is an installed zetup package:
##     __requires__.check()

__extras__ = zfg.EXTRAS

## __notebook__ = zfg.NOTEBOOKS['README']


def setup_entry_point(dist, keyword, value):
    """zetup's `entry_point` handler for `setup()` in a project's _setup.py_,
       setting all setup keyword parameters based on zetup config.

    - Activated with `setup(setup_requires=['zetup'], use_zetup=True)`
    """
    assert keyword == 'use_zetup'
    if not value:
        return

    zetup = Zetup() # reads config from current working directory
                    # (where setup.py is run)
    keywords = zetup.setup_keywords()
    for name, value in keywords.items():
        # Generally, setting stuff on dist.metadata is enough
        # (and necessary), but *pip* only works correct
        # if stuff is also set directly on dist object
        # (seems to read at least packages list somehow from there):
        for obj in [dist, dist.metadata]:
            setattr(obj, name, value)
