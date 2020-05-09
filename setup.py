from setuptools import setup

version = '1.0.10'

with open('requirements.txt') as fd:
    requirements = [line.strip() for line in fd if line.strip()]

testing_requirements = [
    'nose',
    'mock',
    'faker',
    'nosexcover',
    'python-coveralls',
]

linting_requirements = [
    'flake8',
    'pylint',
    'bandit',
]

with open('README.md') as fd:
    long_description = fd.read()

if 'a' in version:
    dev_status = '3 - Alpha'
elif 'b' in version:
    dev_status = '4 - Beta'
else:
    dev_status = '5 - Production/Stable'

setup_args = {
    'name': 'huawei-modem-api-client',
    'version': version,
    'author': 'Pablo Santa Cruz, Mkhanyisi Madlavana',
    'author_email': 'pablo@roshka.com.py, mkhanyisi@gmail.com',
    'url': 'https://github.com/pablo/huawei-modem-python-api-client',
    'download_url': 'https://github.com/dopstar/huawei-modem-python-api-client/tarball/{0}'.format(
        version
    ),
    'package_dir': {'huaweisms': 'huaweisms'},
    'description': 'huaweisms is a python api client for Huawei Modems.',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
    'packages': [
        'huaweisms',
        'huaweisms.api',
        'huaweisms.xml',
    ],
    'data_files': [('', ['requirements.txt'])],
    'install_requires': requirements,
    'tests_require': testing_requirements,
    'extras_require': {
        'testing': testing_requirements,
        'linting': linting_requirements,
    },
    'keywords': ['Huawei', 'Modem', 'HTTP API Client', 'API Client', 'Router'],
    'classifiers': [
        'Development Status :: {0}'.format(dev_status),
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Software Development :: Version Control :: Git',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
}

setup(**setup_args)
