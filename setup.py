from setuptools import find_packages, setup


install_requires = [
    'Django>=1.8,<1.12',
    'tqdm==4.15.0',
    'wagtail>=1.8,<1.13',
]


setup_requires = [
    'setuptools-git-version==1.0.3',
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
    version_format='{tag}.dev{commitcount}+{gitsha}',
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    setup_requires=setup_requires,
    extras_require={
        'testing': testing_extras,
    },
    description=short_description,
    long_description=open('README.rst').read()
)
