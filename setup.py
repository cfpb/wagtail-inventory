from setuptools import find_packages, setup


install_requires = [
    'Django>=1.8,<1.11',
    'wagtail>=1.6,<1.9',
]


testing_extras = [
    'coverage>=3.7.0',
    'flake8>=2.2.0',
    'mock>=1.0.0',
]


short_description = 'Lookup Wagtail pages by block content'


setup(
    name='wagtail-inventory',
    url='https://github.com/cfpb/wagtail-inventory',
    author='CFPB',
    author_email='tech@cfpb.gov',
    license='CCO',
    version='0.1',
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
    },
    description=short_description
)
