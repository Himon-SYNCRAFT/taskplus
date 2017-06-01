from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import codecs
import os
import sys
import re

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Return multiple read calls to different readable objects as a single
    string."""
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(HERE, *parts), 'r').read()

# LONG_DESCRIPTION = read('README.rst')
LONG_DESCRIPTION = ''


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--strict',
            '--verbose',
            '--tb=long',
            'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='taskplus',
    version='1.0.0',
    url='https://github.com/Himon-SYNCRAFT/taskplus',
    license='Apache Software License',
    author='Daniel Zawlocki',
    tests_require=['pytest', 'pytest-cov', 'coverage', 'six'],
    install_requires=[
        'Flask>=0.12.2',
        'SQLAlchemy==1.1.10',
        'pytest-flask>=0.10.0',
        'six',
        ],
    cmdclass={'test': PyTest},
    author_email='d.zawlocki@danielzawlocki.pl',
    description='Example application implementing Clean Architecture',
    long_description=LONG_DESCRIPTION,
    packages=['taskplus'],
    include_package_data=True,
    platforms='any',
    test_suite='tests',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        ],
)
