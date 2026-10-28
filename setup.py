from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in anfac_retail/__init__.py
from anfac_retail import __version__ as version

setup(
	name="anfac_retail",
	version=version,
	description="Anfac Retail",
	author="Anfac Tech",
	author_email="Info@anfactech.so",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
