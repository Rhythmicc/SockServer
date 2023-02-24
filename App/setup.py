from setuptools import setup, find_packages
from App import name, executable_name

with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = "0.0.0"

setup(
    name=name,
    version=VERSION,
    description="< your pypi lib description >",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="< your pypi lib keywords >",
    author="< your name >",
    url="< which url to find your lib >",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["Qpro"],
    entry_points={
        "console_scripts": [
            f"{executable_name} = {name}.main:main",
        ]
    },
)
