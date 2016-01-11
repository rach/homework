import os
import sys
from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages


class ToxCommand(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

here = os.path.abspath(os.path.dirname(__file__))

short_desc = (
    "Application to generate short URL's, manage external links and extract "
    "link info (eg: title, screenshot, content) "
)


install_requires = [
    'pyramid==1.5.7',
    'pyramid-tm==0.12.1',
    'pyramid-services==0.3',
    'pyramid-exclog==0.7',
    'zope.sqlalchemy==0.7.6',
    'Sqlalchemy==1.0.10',
    'schematics==1.1.1',
    'structlog==15.1.0',
    'psycopg2==2.6.1',
    'requests==2.8.1',
    'GeoAlchemy2==0.2.6',
    'waitress==0.8.10',
    'WTForms==2.1',
    'Shapely==1.5.13'
]

tests_require = [
    'tox',
    'pytest-cov',  # before pytest, more info why. See bug #196 in setuptools
    'pytest',
    'webtest'
]


dependency_links = [
]


setup(
    name='homework',
    version='homework',
    description="take home project asked for interview",
    long_description="take home project asked for interview",
    cmdclass={'test': ToxCommand, },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Rachid Belaid',
    author_email='rachid.belaid@gmail.com',
    url='https://github.com/rach/homework',
    packages=find_packages(),
    dependency_links=dependency_links,
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    entry_points="""\
    [console_scripts]
        initialize_db = homework.scripts.initializedb:main
        populate_db = homework.scripts.populatedb:main
    [paste.app_factory]
        api = homework.api:main
    """
)
