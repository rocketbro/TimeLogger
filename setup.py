from setuptools import setup, find_packages

setup(
    name="timelogger",
    version="1.3.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    entry_points={
        "console_scripts": [
            "timelogger=timelogger.main:main",
        ],
    },
)