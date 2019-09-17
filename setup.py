import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
  README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
  name='django-object-status',
  version='0.1',
  packages=find_packages(),
  include_package_data=True,
  liscense='BSD-2-Clause',
  description='A Django app for managing a model object review process',
  long_description=README,
  url='https://github.com/zachtylr21/django-object-status',
  author='Zach Taylor',
  author_email='zachtylr04@gmail.com',
  classifiers=[
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 2.2',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD-2-Clause',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
  ]
)