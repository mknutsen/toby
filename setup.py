from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="sequencer",
    version="1.0",
    description="we will see",
    author="Max Knutsen",
    packages=["sequencer"],
    install_requires=required,  # todo add install requirements mido flask
    entry_points={"console_scripts": ["run-flask-thing=stockcv.flask_entry:main"]},
)
