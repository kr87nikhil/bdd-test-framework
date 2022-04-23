from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='python-bdd',
    version='1.3',
    author='nikhil',
    description='Python test automation framework implementation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/kr87nikhil/python-bdd',
    packages=find_packages(
        include=[
            "app",
            "app_aws",
            "relational",
            "non-relational"
        ]
    ),
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
    ]
)
