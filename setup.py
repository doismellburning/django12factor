import os
import sys
from setuptools import setup, find_packages

__version__ = '0.1'

HERE = os.path.dirname(__file__)

requirements = open(os.path.join(HERE, 'requirements.txt')).readlines()
if sys.version_info[:2] < (2, 7):
    requirements.append('argparse')

try:
    long_description = open(os.path.join(HERE, 'README.md')).read()
except:
    long_description = None

setup(
    name='django12factor',
    version=__version__,
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    zip_safe=True,

    # metadata for upload to PyPI
    author='Kristian Glass',
    author_email='django12factor@doismellburning.co.uk',
    url='https://github.com/doismellburning/django12factor',
    description='django12factor: Bringing 12factor to Django',
    long_description=long_description,
    license='MIT',
    keywords='django 12factor configuration',

    install_requires=requirements,

    classifiers=(
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ),
)
