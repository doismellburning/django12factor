import os
from setuptools import setup, find_packages

__version__ = '1.3'

HERE = os.path.dirname(__file__)

try:
    long_description = open(os.path.join(HERE, 'README.rst')).read()
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

    install_requires=(
        "dj-database-url==0.3.0",
        "dj-email-url==0.0.2",
        "django-cache-url==0.8.0",
        "six",
    ),

    tests_require=(
        "nose",
    ),
    test_suite='nose.collector',

    classifiers=(
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ),

)
