from setuptools import setup

version = '1.0.2'

with open('requirements.txt') as fd:
    requirements = [line.strip() for line in fd if line.strip()]

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
    'download_url': 'https://github.com/pablo/huawei-modem-python-api-client/tarball/{0}'.format(
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
    'keywords': 'Huawei Modem API',
    'classifiers': [
        'Development Status :: {0}'.format(dev_status),
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
}

setup(**setup_args)
