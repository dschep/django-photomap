from setuptools import setup
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='photomap',

    version='0.1.0',

    description='A simple Django app to provide a map with user submitted phots',
    long_description=long_description,

    url='https://github.com/dschep/django-photomap',

    author='Daniel Schep',
    author_email='dschep@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'Topic :: Software Development :: Build Tools',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics :: Presentation',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='django photos images maps',

    packages=['photomap'],

    install_requires=[
        'Django',
        'Pillow',
        'South',
        'django-tastypie',
        'six',
        'django-stdimage',
        'django-appconf',
        ],

    package_data={
        'photomap': ['static/photomap/*/*', 'templates/photomap/*'],
    },
)
