from setuptools import setup

setup(name='pyanoboard',
      version='0.1.0',
      description='Simple piano to keyboard adaptor. Works with any MIDI enabled device.',
      url='https://github.com/QFSW/Pyanoboard',
      author='QFSW',
      author_email='support@qfsw.co.uk',
      license='MIT',
      packages=['pyanoboard'],
      zip_safe=False,
      install_requires=[
            'pygame',
      ])
