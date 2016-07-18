#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages


setup(
    name='django-datatable',
    version='0.2.1',
    author='shymonk',
    author_email='hellojohn201@gmail.com',
    url='https://github.com/shymonk/django-datatable',
    description='A simple Django app to origanize data in tabular form.',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['test*', 'example*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=["django>=1.5"],
    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
