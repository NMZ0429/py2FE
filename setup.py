from setuptools import setup

setup(
    install_requires=["cryptography"],
    entry_points={"console_scripts": ["tfc = main:main"]},
    name="two_factor_cryptor",
    version="0.0.1",
)

