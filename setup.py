""" Setup script for the Control Version Manager project."""
from setuptools import setup, find_packages

setup(
    name="control-version-manager",
    version="0.1.0",
    author="Mateusz Wojcik",
    author_email="mateuszwojcikv@gmail.com",
    description="A version control manager for 3D files.",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/agh-space-systems-mechanics/control-version-manager",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "CustomTkinter",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
