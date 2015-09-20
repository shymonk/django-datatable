import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-datatable',
    version='0.1.4',
    author='shymonk',
    author_email='hellojohn201@gmail.com',
    url='https://github.com/shymonk/django-datatable',
    description='A simple Django app to origanize data in tabular form.',
    long_description=README,
    packages=find_packages(exclude=['test*', 'example*']),
    include_package_data=True,
    zip_safe = False,
    install_requires=["django>=1.5"],
    license='BSD License',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

