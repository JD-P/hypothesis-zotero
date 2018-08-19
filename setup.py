from setuptools import setup, find_packages

setup(
    name="hypothesis-zotero",
    version="0.1",
    install_requires=['pyzotero>=1.3.6','python-hypothesis'],
    #TODO: Change this to upstream dependency once upstream merges some kind of python3 compatibility
    dependency_links=['git+https://github.com/JD-P/python-hypothesis.git#egg=python-hypothesis'],
    author="John David Pressman",
    author_email="jd@jdpressman.com",
    description="This program scans through a Zotero library and checks each URL for Hypothesis annotations. If annotations are found it imports them into the Zotero library as note objects with their associated tags.",
    license="MIT",
    url="https://github.com/JD-P/hypothesis-zotero")
    
