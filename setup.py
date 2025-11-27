from setuptools import setup, find_packages

setup(
    name="fortran-ode-solver",
    version="0.1.0",
    description="Python wrapper for Fortran ODE solver",
    author="Xavier Ramos",
    author_email="xarnyc@protonmail.com",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ode-solve=python.cli:cli",
        ],
    },
    python_requires=">=3.9",
)
