import sys
import os
import datetime
from setuptools import setup, find_packages

name='silpa'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description=(
        read('README')
        + '\n' 
        )

setup(
    name=name,
    version=datetime.datetime.now().strftime("%Y%m%d"),
    url='http://smc.org.in/silpa',
    license='AGPL 3.0',
    description='Indic Language Computing Library',
    author='Santhosh Thottingal',
    author_email='santhosh.thottingal@gmail.com',
    long_description=long_description,
    include_package_data=True,
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    package_data = {'': ['doc']},
    namespace_packages=['silpa'],
    install_requires=['setuptools'],
    zip_safe = True,
    )
