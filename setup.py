"""Setup module for aioairzone-cloud."""
from pathlib import Path

from setuptools import setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
VERSION = "0.0.1"


setup(
    name="aioairzone-cloud",
    version=VERSION,
    url="https://github.com/Noltari/aioairzone-cloud",
    download_url="https://github.com/Noltari/aioairzone-cloud",
    author="Álvaro Fernández Rojas",
    author_email="noltari@gmail.com",
    description="Library to control Airzone Cloud devices",
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=["aioairzone_cloud"],
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=["aiohttp"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Home Automation",
    ],
)
