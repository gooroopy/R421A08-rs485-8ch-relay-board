#!/usr/bin/env python

from distutils.core import setup

setup(name='R421AXX-modbus-relay',
      version='1.0',
      description='R421AXX relay board control',
      author='Suriyan Laohaprapanon',
      author_email='suriyant@gmail.com',
      url='https://github.com/gooroopy/R421A08-rs485-8ch-relay-board',
      packages=['relay_boards', 'relay_modbus', 'print_stderr'],
      install_requires=[
          'pyserial',
      ],
     )
