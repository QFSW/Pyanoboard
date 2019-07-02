from setuptools import setup


from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='pyanoboard',
      version='1.0.3',
      description='Pyanoboard is a simple piano to keyboard emulator, allowing you to use any MIDI enabled device as a virtual keyboard.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/QFSW/Pyanoboard',
      author='QFSW',
      author_email='support@qfsw.co.uk',
      license='MIT',
      packages=['pyanoboard'],
      install_requires=[
            'pygame',
      ])
