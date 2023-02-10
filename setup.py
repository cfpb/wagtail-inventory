from setuptools import find_packages, setup


install_requires = [
    "tqdm>=4.15.0,<5",
    "wagtail>=4.1",
]


testing_extras = [
    "coverage>=3.7.0",
    "mock>=1.0.0",
]

setup(
    name="wagtail-inventory",
    url="https://github.com/cfpb/wagtail-inventory",
    author="CFPB",
    author_email="tech@cfpb.gov",
    description="Lookup Wagtail pages by block content",
    long_description=open("README.rst", "r", encoding="utf-8").read(),
    license="CCO",
    version="1.6",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require={"testing": testing_extras},
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 4",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
