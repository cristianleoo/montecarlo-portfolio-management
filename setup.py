from setuptools import setup, find_packages

setup(
    name='portfolio_management',
    version='1.0.0',
    description='Portfolio Management with Monte Carlo Simulation',
    author='Cristian Leo',
    author_email='cristianleo120@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'pandas>=1.0.0',
        'scipy>=1.4.0',
        'matplotlib>=3.1.0',
    ],
)
