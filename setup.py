# pip install -e .

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="user-research-helper",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=requirements,
)