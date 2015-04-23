from textwrap import dedent
from warnings import warn

from zetup import Zetup


zetup = Zetup()

setup = zetup.setup
setup['package_data']['zetup.commands.make'] = [
  'templates/*.jinja',
  'templates/package/*.jinja',
  ]
setup(
  ## setup_requires=['hgdistver >= 0.23'],

  ## get_version_from_scm=True,

  entry_points={
    'distutils.setup_keywords': [
      'use_zetup = zetup:setup_entry_point',
      ],
    'console_scripts': [
      'zetup = zetup.script:run',
      ]},
  )
