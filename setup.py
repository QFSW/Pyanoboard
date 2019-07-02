from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pyanoboard',
      version='0.1.1',
      description='Pyanoboard is a simple piano to keyboard emulator, allowing you to use any MIDI enabled device as a virtual keyboard.',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://github.com/QFSW/Pyanoboard',
      author='QFSW',
      author_email='support@qfsw.co.uk',
      license='MIT',
      packages=['pyanoboard'],
      install_requires=[
            'pygame',
      ],
      entry_points={
            "console_scripts": [
                  "pyanoboard=pyanoboard.__main__:main",
            ]
      })
