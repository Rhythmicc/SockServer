from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = "0.0.6"

setup(
    name='SockServer',
    version=VERSION,
    description='Socket Server with ThreadPool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='Socket Server with ThreadPool',
    author='RhythmLian',
    author_mail='RhythmLian@outlook.com',
    url="https://github.com/Rhythmicc/SockServer",
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['rich'],
    # entry_points={},
)
