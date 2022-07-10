from setuptools import find_packages, setup

setup(
    name="mysequencer",
    version="1.0",
    description="we will see",
    author="Max Knutsen",
    packages=find_packages(include=['mysequencer']),
    install_requires=['mido',],  # todo add install requirements mido flask
)
