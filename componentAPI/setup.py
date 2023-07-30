import os
from setuptools import setup

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "componentAPI",
    version = "0.0.4",
    author = "JannikB5825",
    author_email = "givknive@gmail.com",
    description = ("An API for storing electronic components"),
    license = "MIT",
    url = "https://github.com/JannikB5825/ComponentManager",
    packages=['api'],
    long_description=read('README'),
    install_requires=[
        "fastapi",
        "uvicorn",
        "requests"
    ]
)