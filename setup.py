from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import codecs
import os
import sys


HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Return multiple read calls to different readable objects as a single
    string."""
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
    license='BSD',
    author='Daniel Zawlocki',
    tests_require=[
        'pytest',
        'pytest-cov',
        'coverage',
        'six',
        'pytest-flask'
    ],
    install_requires=[
        'Flask>=0.12.2',
        'Flask-Script>=2.0.5',
        'Flask-Login>=0.4.0',
        'SQLAlchemy==1.1.10',
        'pytest-flask>=0.10.0',
        'six',
        'bcrypt>=3.1.3',
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
)
