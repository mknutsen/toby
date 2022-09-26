from setuptools import find_packages, setup

setup(
    name="toby",
    version="1.0",
    description="we will see",
    author="Max Knutsen",
    packages=find_packages(include=['toby']),
    install_requires=['mido',],  # todo add install requirements mido flask
)
