import codecs
import os
from setuptools import find_packages, setup

# Constants
PACKAGE_NAME = "py3utilities"
PACKAGE_VERSION = "0.0.6"
AUTHOR_NAME = "Nishant Rao"
AUTHOR_EMAIL_ID = "nishant.rao173@gmail.com"
FILEPATH_TO_README = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")

# Requirements
install_requires = []
with open(file="requirements.txt", mode="r") as fp:
    install_requires.extend(
        [s for s in [line.strip(" \n") for line in fp] if not s.startswith("#") and s != ""]
    )

# Documentation
long_description = ""
with codecs.open(filename=FILEPATH_TO_README, encoding="utf-8") as fh:
    long_description += "\n" + fh.read()

# Setup
setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description="Library having Python utility code",
    long_description=long_description,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL_ID,
    url="https://github.com/Nishant173/pyutils/",
    packages=find_packages(where="."),
    include_package_data=True,
    install_requires=install_requires,
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
